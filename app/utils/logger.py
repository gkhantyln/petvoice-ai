# app/utils/logger.py
# Uygulama loglama ve izleme yardımcı fonksiyonları
# Bu dosya, uygulama genelinde loglama ve izleme işlemlerini içerir

import logging
import os
from logging.handlers import RotatingFileHandler
from flask import request, current_app
from datetime import datetime

def setup_logging(app):
    """
    Uygulama loglamasını yapılandırır
    """
    if not app.debug and not app.testing:
        # Log dizinini oluştur
        if not os.path.exists('logs'):
            os.mkdir('logs')
        
        # Dosya log handler'ı
        file_handler = RotatingFileHandler(
            'logs/petvoice.log', 
            maxBytes=10240000,  # 10MB
            backupCount=10
        )
        
        # Log formatı
        formatter = logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        )
        file_handler.setFormatter(formatter)
        file_handler.setLevel(logging.INFO)
        
        # Handler'ı uygulamaya ekle
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('PetVoice AI başlatıldı')

def log_user_activity(user_id, action, details=None):
    """
    Kullanıcı aktivitesini loglar
    """
    current_app.logger.info(f"User {user_id}: {action} - {details}")

def log_analysis_activity(analysis_id, status, details=None):
    """
    Analiz aktivitesini loglar
    """
    current_app.logger.info(f"Analysis {analysis_id}: {status} - {details}")

def log_error(error, context=None):
    """
    Hataları loglar
    """
    current_app.logger.error(f"Error: {error} - Context: {context}")