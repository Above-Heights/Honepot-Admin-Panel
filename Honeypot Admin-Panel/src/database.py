# src/database.py
import sqlite3
import hashlib
import random
import string
from config import Config

def init_database(db_path=None):
    """Initialize the database with fake data"""
    if db_path is None:
        db_path = Config.DATABASE_PATH
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Users table with intentional SQLi vulnerability
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE,
            password TEXT,
            email TEXT,
            role TEXT,
            last_login TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # System logs table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS system_logs (
            id INTEGER PRIMARY KEY,
            ip_address TEXT,
            user_agent TEXT,
            action TEXT,
            timestamp TEXT,
            vulnerability_type TEXT,
            payload TEXT,
            severity TEXT
        )
    ''')
    
    # Fake sensitive data
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sensitive_data (
            id INTEGER PRIMARY KEY,
            credit_card TEXT,
            ssn TEXT,
            secret_key TEXT,
            department TEXT,
            salary TEXT
        )
    ''')
    
    # Attack patterns table for analysis
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS attack_patterns (
            id INTEGER PRIMARY KEY,
            pattern_name TEXT,
            payload TEXT,
            vulnerability_type TEXT,
            severity TEXT,
            description TEXT
        )
    ''')
    
    # Insert default users
    insert_default_data(cursor)
    
    conn.commit()
    conn.close()
    print(f"Database initialized at: {db_path}")

def insert_default_data(cursor):
    """Insert default fake data into the database"""
    
    # Default admin user (you can change these credentials)
    default_users = [
        {
            'username': 'admin',
            'password': 'admin123',  # Change this
            'email': 'admin@company.com',
            'role': 'administrator'
        },
        {
            'username': 'john_doe', 
            'password': 'password123',
            'email': 'john.doe@company.com',
            'role': 'user'
        },
        {
            'username': 'sarah_smith',
            'password': 'welcome1',
            'email': 'sarah.smith@company.com', 
            'role': 'manager'
        },
        {
            'username': 'test_user',
            'password': 'test123',
            'email': 'test@company.com',
            'role': 'user'
        },
        # Add more users as needed
        {
            'username': 'root',
            'password': 'toor',
            'email': 'root@system.com',
            'role': 'administrator'
        }
    ]
    
    for user_data in default_users:
        hashed_password = hashlib.md5(user_data['password'].encode()).hexdigest()
        try:
            cursor.execute(
                "INSERT INTO users (username, password, email, role) VALUES (?, ?, ?, ?)",
                (user_data['username'], hashed_password, user_data['email'], user_data['role'])
            )
        except sqlite3.IntegrityError:
            pass  # User already exists
    
    # Fake sensitive data
    sensitive_data = [
        ("4532015112830366", "123-45-6789", "SECRET-KEY-001", "Finance", "$120,000"),
        ("5506922406242714", "987-65-4321", "API-KEY-SPECIAL-2024", "IT", "$95,000"),
        ("371449635398431", "456-78-9012", "PRIVATE-TOKEN-XYZ", "HR", "$85,000"),
        ("6011111111111117", "111-22-3333", "ENCRYPTION-KEY-007", "Security", "$150,000"),
        ("5105105105105100", "555-66-7777", "DATABASE-PASSWORD", "Engineering", "$110,000")
    ]
    
    for data in sensitive_data:
        try:
            cursor.execute(
                "INSERT INTO sensitive_data (credit_card, ssn, secret_key, department, salary) VALUES (?, ?, ?, ?, ?)",
                data
            )
        except:
            pass
    
    # Pre-populate attack patterns
    attack_patterns = [
        ("Basic SQL Injection", "' OR '1'='1' --", "SQLi", "High", "Classic authentication bypass"),
        ("Union SQL Injection", "' UNION SELECT 1,2,3 --", "SQLi", "High", "Data extraction technique"),
        ("XSS Script", "<script>alert('XSS')</script>", "XSS", "Medium", "Basic cross-site scripting"),
        ("XSS Image", "<img src=x onerror=alert(1)>", "XSS", "Medium", "XSS using image error handler"),
        ("Command Injection", "; ls -la", "Command Injection", "Critical", "OS command injection attempt")
    ]
    
    for pattern in attack_patterns:
        try:
            cursor.execute(
                "INSERT INTO attack_patterns (pattern_name, payload, vulnerability_type, severity, description) VALUES (?, ?, ?, ?, ?)",
                pattern
            )
        except:
            pass

def add_new_user(username, password, email, role="user"):
    """Helper function to add new users to the database"""
    conn = sqlite3.connect(Config.DATABASE_PATH)
    cursor = conn.cursor()
    
    hashed_password = hashlib.md5(password.encode()).hexdigest()
    
    try:
        cursor.execute(
            "INSERT INTO users (username, password, email, role) VALUES (?, ?, ?, ?)",
            (username, hashed_password, email, role)
        )
        conn.commit()
        print(f"User '{username}' added successfully")
    except sqlite3.IntegrityError:
        print(f"User '{username}' already exists")
    finally:
        conn.close()

def reset_database():
    """Reset the database to initial state (for testing)"""
    import os
    if os.path.exists(Config.DATABASE_PATH):
        os.remove(Config.DATABASE_PATH)
    init_database()
    print("Database reset complete")

if __name__ == '__main__':
    init_database()