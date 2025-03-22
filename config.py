import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    APP_PASSWORD = os.getenv('APP_PASSWORD', 'your-strong-password')