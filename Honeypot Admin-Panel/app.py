from flask import Flask, render_template, request, session, redirect, url_for, flash
import sqlite3
import hashlib
import datetime
import html
import re

app = Flask(__name__)
app.secret_key = 'honeypot_secret_key_123'  # Intentionally weak

# Initialize database
from database import init_database
init_database()

def log_attack(ip, user_agent, action, vuln_type):
    """Log attack attempts for analysis"""
    conn = sqlite3.connect('honeypot.db')
    cursor = conn.cursor()
    timestamp = datetime.datetime.now().isoformat()
    
    cursor.execute(
        "INSERT INTO system_logs (ip_address, user_agent, action, timestamp, vulnerability_type) VALUES (?, ?, ?, ?, ?)",
        (ip, user_agent, action, timestamp, vuln_type)
    )
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    # Intentional SQL Injection vulnerability
    if request.method == 'POST':
        username = request.form['username']
        password = hashlib.md5(request.form['password'].encode()).hexdigest()
        
        # VULNERABLE SQL QUERY - No parameterization
        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
        
        conn = sqlite3.connect('honeypot.db')
        cursor = conn.cursor()
        
        try:
            cursor.execute(query)
            user = cursor.fetchone()
            
            if user:
                session['user_id'] = user[0]
                session['username'] = user[1]
                session['role'] = user[4]
                
                log_attack(request.remote_addr, request.headers.get('User-Agent'), 
                          f"Successful login: {username}", "SQLi Attempt")
                
                return redirect(url_for('dashboard'))
            else:
                flash('Invalid credentials!')
                log_attack(request.remote_addr, request.headers.get('User-Agent'), 
                          f"Failed login attempt: {username}", "Authentication Failure")
        except Exception as e:
            flash('Database error occurred')
            log_attack(request.remote_addr, request.headers.get('User-Agent'), 
                      f"SQL Error: {str(e)}", "SQLi Exploit")
        finally:
            conn.close()
    
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    return render_template('dashboard.html', username=session['username'])

@app.route('/users')
def users():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    search = request.args.get('search', '')
    conn = sqlite3.connect('honeypot.db')
    cursor = conn.cursor()
    
    # VULNERABLE: SQL Injection in search
    if search:
        query = f"SELECT id, username, email, role, last_login FROM users WHERE username LIKE '%{search}%' OR email LIKE '%{search}%'"
        log_attack(request.remote_addr, request.headers.get('User-Agent'), 
                  f"User search with: {search}", "SQLi Attempt")
    else:
        query = "SELECT id, username, email, role, last_login FROM users"
    
    cursor.execute(query)
    users_data = cursor.fetchall()
    conn.close()
    
    # Intentional XSS vulnerability - not escaping user input
    return render_template('users.html', users=users_data, search_query=search)

@app.route('/user_profile')
def user_profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    # VULNERABLE: Reflected XSS
    user_id = request.args.get('id', '')
    message = request.args.get('message', '')
    
    conn = sqlite3.connect('honeypot.db')
    cursor = conn.cursor()
    cursor.execute("SELECT username, email, role FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    
    if user:
        log_attack(request.remote_addr, request.headers.get('User-Agent'), 
                  f"Profile view with params: id={user_id}, message={message}", "XSS Attempt")
    
    # Intentionally not escaping the message parameter for XSS vulnerability
    return render_template('user_profile.html', user=user, message=message)

@app.route('/sensitive_data')
def sensitive_data():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    # Fake sensitive data endpoint
    conn = sqlite3.connect('honeypot.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM sensitive_data")
    data = cursor.fetchall()
    conn.close()
    
    log_attack(request.remote_addr, request.headers.get('User-Agent'), 
              "Accessed sensitive data", "Data Access")
    
    return render_template('sensitive_data.html', data=data)

@app.route('/logs')
def view_logs():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = sqlite3.connect('honeypot.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM system_logs ORDER BY timestamp DESC LIMIT 100")
    logs = cursor.fetchall()
    conn.close()
    
    return render_template('logs.html', logs=logs)

@app.route('/search')
def search():
    # VULNERABLE: Stored XSS in search results
    query = request.args.get('q', '')
    
    conn = sqlite3.connect('honeypot.db')
    cursor = conn.cursor()
    
    # Log the search query without sanitization (for stored XSS demonstration)
    if query:
        cursor.execute(
            "INSERT INTO system_logs (ip_address, user_agent, action, timestamp, vulnerability_type) VALUES (?, ?, ?, ?, ?)",
            (request.remote_addr, request.headers.get('User-Agent'), f"Search: {query}", 
             datetime.datetime.now().isoformat(), "XSS Attempt")
        )
        conn.commit()
    
    conn.close()
    
    # Intentionally vulnerable to reflected XSS
    return f"<h2>Search Results for: {query}</h2><p>No results found.</p>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)  # Debug mode on intentionally 