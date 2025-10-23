# config.py
import os
from datetime import timedelta

class Config:
    # Security
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'costbyte-military-grade-encryption-2024'
    SECURITY_PASSWORD_SALT = os.environ.get('SECURITY_PASSWORD_SALT') or 'costbyte-supersecret-salt'
    
    # Database
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///costbyte.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # FNB Bank Accounts
    FNB_ACCOUNTS = {
        'owner': '6212345678901',
        'ai_operations': '6212345678902', 
        'reserve': '6212345678903'
    }
    
    # Payment Configuration
    PAYMENT_DISTRIBUTION = {
        'owner': 0.60,      # 60%
        'ai_operations': 0.20,  # 20%
        'reserve': 0.20     # 20%
    }
    
    # Revenue Targets
    REVENUE_TARGETS = {
        'week_1_subscribers': 5000,
        'month_1_revenue_zar': 25000000,
        'month_3_revenue_zar': 50000000, 
        'month_6_revenue_zar': 100000000,
        'year_1_revenue_zar': 500000000
    }
    
    # Social Media APIs
    SOCIAL_MEDIA_KEYS = {
        'linkedin': os.environ.get('LINKEDIN_API_KEY'),
        'tiktok': os.environ.get('TIKTOK_API_KEY'),
        'instagram': os.environ.get('INSTAGRAM_API_KEY'),
        'facebook': os.environ.get('FACEBOOK_API_KEY'),
        'youtube': os.environ.get('YOUTUBE_API_KEY'),
        'x': os.environ.get('X_API_KEY')
    }
    
    # AI Model Configuration
    AI_MODELS = {
        'llm_chatbot': 'gpt-4',
        'content_creation': 'gpt-4',
        'analytics': 'custom-ml-model'
    }
    
    # Upload Configuration
    UPLOAD_FOLDER = 'static/uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size

class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    DEBUG = False
    TESTING = False

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
