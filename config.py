# config.py
# Uygulama yapılandırma ayarları
# Bu dosya, farklı ortamlar için yapılandırma ayarlarını içerir

import os
from datetime import timedelta

class Config:
    """Temel yapılandırma sınıfı"""
    # Gizli anahtar (üretim ortamında environment variable olarak ayarlayın)
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'gizli-anahtar-varsayilan-deger'
    
    # Veritabanı yapılandırması - varsayılan olarak SQLite kullan
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(os.path.dirname(__file__), 'petvoice.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Dosya yükleme ayarları
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER') or 'uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB maksimum dosya boyutu
    
    # Oturum ayarları
    PERMANENT_SESSION_LIFETIME = timedelta(hours=1)
    
    # E-posta yapılandırması (Flask-Mail için)
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 587)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    
    # AI API anahtarı
    GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')
    
    # Celery yapılandırması
    CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL') or 'redis://localhost:6379/0'
    CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND') or 'redis://localhost:6379/0'

class DevelopmentConfig(Config):
    """Geliştirme ortamı yapılandırması"""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(os.path.dirname(__file__), 'petvoice_dev.db')

class TestingConfig(Config):
    """Test ortamı yapılandırması"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite:///' + os.path.join(os.path.dirname(__file__), 'tests/test.db')

class ProductionConfig(Config):
    """Üretim ortamı yapılandırması"""
    DEBUG = False
    # Üretim ortamında PostgreSQL kullan
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'postgresql://kullanici:sifre@localhost/petvoice'

# Yapılandırma sınıflarını dictionary olarak tanımla
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}