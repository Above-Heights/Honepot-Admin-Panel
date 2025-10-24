# src/config.py
import os

class Config:
    """Configuration settings for the honeypot"""
    
    # Server Configuration
    HOST = '0.0.0.0'
    PORT = 5000  # Change this to your desired port
    DEBUG = True
    
    # Database Configuration
    DATABASE_PATH = 'honeypot.db'
    
    # Security Configuration (Intentionally weak)
    SECRET_KEY = 'honeypot_secret_key_123'
    SESSION_TIMEOUT = 3600  # 1 hour
    
    # Honeypot Settings
    HONEYPOT_NAME = "Project Aegis Honeycomb"
    ADMIN_EMAIL = "admin@honeypot.local"
    
    # Logging Configuration
    LOG_LEVEL = 'INFO'
    LOG_FILE = 'logs/honeypot.log'

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    PORT = 5000  # Development port

class ProductionConfig(Config):
    """Production configuration (for isolated environments)"""
    DEBUG = False
    PORT = 8080  # Different port for production
    HOST = '127.0.0.1'  # Only localhost in production

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    PORT = 5999  # Test port
    DATABASE_PATH = 'test_honeypot.db'

# Configuration selector
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}