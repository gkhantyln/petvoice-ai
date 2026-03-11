# init_uploads.py
# Upload dizinlerini başlatıcı
# Bu dosya, ses dosyaları ve spektrogramlar için gerekli dizinleri oluşturur

import os
from app import create_app

def init_upload_directories():
    """Upload dizinlerini başlatır"""
    # Uygulamayı oluştur
    app = create_app(os.getenv('FLASK_CONFIG') or 'default')
    
    with app.app_context():
        # Upload klasörünü al
        upload_folder = app.config['UPLOAD_FOLDER']
        
        # Upload klasörünün tam yolunu al
        upload_folder = os.path.abspath(upload_folder)
        
        # Gerekli alt dizinleri oluştur
        sounds_dir = os.path.join(upload_folder, 'sounds')
        spectrograms_dir = os.path.join(upload_folder, 'spectrograms')
        
        # Windows uyumluluğu için tam yolları kullan
        sounds_dir = os.path.abspath(sounds_dir)
        spectrograms_dir = os.path.abspath(spectrograms_dir)
        
        # Dizinleri oluştur
        os.makedirs(sounds_dir, exist_ok=True)
        os.makedirs(spectrograms_dir, exist_ok=True)
        
        print(f"Upload dizinleri oluşturuldu:")
        print(f"  Ses dosyaları: {sounds_dir}")
        print(f"  Spektrogramlar: {spectrograms_dir}")

if __name__ == '__main__':
    init_upload_directories()