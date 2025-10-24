# src/utils/db_manager.py
import sqlite3
from database import init_database, add_new_user, reset_database
from config import Config

def show_database_stats():
    """Show statistics about the database"""
    conn = sqlite3.connect(Config.DATABASE_PATH)
    cursor = conn.cursor()
    
    # Count users
    cursor.execute("SELECT COUNT(*) FROM users")
    user_count = cursor.fetchone()[0]
    
    # Count logs
    cursor.execute("SELECT COUNT(*) FROM system_logs")
    log_count = cursor.fetchone()[0]
    
    # Count attacks by type
    cursor.execute("SELECT vulnerability_type, COUNT(*) FROM system_logs GROUP BY vulnerability_type")
    attack_stats = cursor.fetchall()
    
    print(f"Database: {Config.DATABASE_PATH}")
    print(f"Total Users: {user_count}")
    print(f"Total Attack Logs: {log_count}")
    print("Attack Statistics:")
    for vuln_type, count in attack_stats:
        print(f"  {vuln_type}: {count}")
    
    conn.close()

def export_attack_logs(output_file='attack_logs.csv'):
    """Export attack logs to CSV"""
    import csv
    conn = sqlite3.connect(Config.DATABASE_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM system_logs")
    logs = cursor.fetchall()
    
    with open(output_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['ID', 'IP Address', 'User Agent', 'Action', 'Timestamp', 'Vulnerability', 'Payload', 'Severity'])
        writer.writerows(logs)
    
    print(f"Logs exported to: {output_file}")
    conn.close()

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Database Management Utility')
    parser.add_argument('--reset', action='store_true', help='Reset database to initial state')
    parser.add_argument('--stats', action='store_true', help='Show database statistics')
    parser.add_argument('--export', action='store_true', help='Export attack logs to CSV')
    parser.add_argument('--add-user', nargs=3, metavar=('USERNAME', 'PASSWORD', 'EMAIL'), 
                       help='Add a new user to the database')
    
    args = parser.parse_args()
    
    if args.reset:
        reset_database()
    elif args.stats:
        show_database_stats()
    elif args.export:
        export_attack_logs()
    elif args.add_user:
        username, password, email = args.add_user
        add_new_user(username, password, email)
    else:
        print("Use --help to see available options")