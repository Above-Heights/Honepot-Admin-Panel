# 🍯 Honeypot Admin Panel - Cybersecurity Research Project

> **⚠️ SECURITY WARNING: FOR EDUCATIONAL/RESEARCH USE ONLY**
> This project contains intentional vulnerabilities and should NEVER be deployed in production environments.

## 📖 Overview

A deliberately vulnerable admin panel system designed as a honeypot to study and analyze cyber attacks. This project demonstrates common web vulnerabilities in a controlled environment for security research and educational purposes.

## 🎯 Purpose

- **Security Research**: Study attack patterns and techniques
- **Education**: Learn about web application vulnerabilities
- **Testing**: Evaluate security tools and monitoring systems
- **Honeypot Operation**: Attract and analyze malicious activity

## 🔍 Intentional Vulnerabilities

- **SQL Injection (SQLi)**: Multiple unsanitized user inputs
- **Cross-Site Scripting (XSS)**: Reflected and stored XSS vulnerabilities
- **Weak Authentication**: MD5 hashing, predictable credentials
- **Information Disclosure**: Detailed error messages

## 🛡️ Security Features

- Comprehensive attack logging
- IP address tracking
- Vulnerability classification
- Fake sensitive data for attacker engagement

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Flask

### Installation
```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/honeypot-admin-panel.git
cd honeypot-admin-panel

# Install dependencies
pip install -r requirements.txt

# Initialize database
python database.py

# Start the honeypot
python app.py 