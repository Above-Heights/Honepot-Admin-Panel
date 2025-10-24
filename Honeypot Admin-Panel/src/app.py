# src/app.py
from flask import Flask, render_template, request, session, redirect, url_for, flash
import sqlite3
import hashlib
import datetime
from config import config

app = Flask(__name__)
app.config.from_object(config['development'])  # Change to 'production' for production

# Import and initialize database
from database import init_database, reset_database
init_database()

def log_attack(ip, user_agent, action, vuln_type, payload=""):
    """Log attack attempts for analysis"""
    conn = sqlite3.connect(app.config['DATABASE_PATH'])
    cursor = conn.cursor()
    timestamp = datetime.datetime.now().isoformat()
    
    # Determine severity
    severity = "Low"
    if "SQL" in vuln_type.upper() or "XSS" in vuln_type.upper():
        severity = "High"
    elif "Command" in vuln_type or "File" in vuln_type:
        severity = "Critical"
    
    cursor.execute(
        """INSERT INTO system_logs 
        (ip_address, user_agent, action, timestamp, vulnerability_type, payload, severity) 
        VALUES (?, ?, ?, ?, ?, ?, ?)""",
        (ip, user_agent, action, timestamp, vuln_type, str(payload)[:500], severity)
    )
    conn.commit()
    conn.close()

# ... rest of your routes remain the same ...

if __name__ == '__main__':
    # Use configuration from config.py
    app.run(
        host=app.config['HOST'],
        port=app.config['PORT'], 
        debug=app.config['DEBUG']
    )