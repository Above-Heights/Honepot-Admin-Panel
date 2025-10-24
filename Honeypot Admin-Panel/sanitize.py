# sanitize.py
import re

def sanitize_file(filename):
    with open(filename, 'r') as file:
        content = file.read()
    
    # Replace sensitive values
    content = content.replace("'honeypot_secret_key_123'", "'SANITIZED_SECRET_KEY'")
    content = content.replace("admin123", "SANITIZED_PASSWORD")
    content = re.sub(r"host='.*?'", "host='SANITIZED_HOST'", content)
    content = re.sub(r"port='.*?'", "port='SANITIZED_PORT'", content)
    
    with open(filename, 'w') as file:
        file.write(content)

# Sanitize all Python files
files_to_sanitize = ['app.py', 'database.py']
for file in files_to_sanitize:
    sanitize_file(file)
    print(f"Sanitized: {file}") 