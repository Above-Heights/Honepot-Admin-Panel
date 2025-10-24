import sqlite3
import hashlib
import random
import string

def init_database():
    conn = sqlite3.connect('honeypot.db')
    cursor = conn.cursor()
    
    # Users table with intentional SQLi vulnerability
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE,
            password TEXT,
            email TEXT,
            role TEXT,
            last_login TEXT
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
            vulnerability_type TEXT
        )
    ''')
    
    # Fake sensitive data
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sensitive_data (
            id INTEGER PRIMARY KEY,
            credit_card TEXT,
            ssn TEXT,
            secret_key TEXT
        )
    ''')
    
    # Insert default admin user
    admin_password = hashlib.md5("admin123".encode()).hexdigest()  # Weak hashing intentionally
    try:
        cursor.execute("INSERT INTO users (username, password, email, role) VALUES (?, ?, ?, ?)",
                      ("admin", admin_password, "admin@honeypot.local", "administrator"))
    except:
        pass
    
    # Insert fake users
    fake_users = [
        ("john_doe", hashlib.md5("password123".encode()).hexdigest(), "john@company.com", "user"),
        ("sarah_smith", hashlib.md5("welcome1".encode()).hexdigest(), "sarah@company.com", "admin"),
        ("test_user", hashlib.md5("test".encode()).hexdigest(), "test@test.com", "user")
    ]
    
    for user in fake_users:
        try:
            cursor.execute("INSERT INTO users (username, password, email, role) VALUES (?, ?, ?, ?)", user)
        except:
            pass
    
    # Insert fake sensitive data
    fake_data = [
        ("4532015112830366", "123-45-6789", "SECRET-KEY-001"),
        ("5506922406242714", "987-65-4321", "API-KEY-SPECIAL-2024"),
        ("371449635398431", "456-78-9012", "PRIVATE-TOKEN-XYZ")
    ]
    
    for data in fake_data:
        try:
            cursor.execute("INSERT INTO sensitive_data (credit_card, ssn, secret_key) VALUES (?, ?, ?)", data)
        except:
            pass
    
    conn.commit()
    conn.close()

def get_db_connection():
    return sqlite3.connect('honeypot.db') 