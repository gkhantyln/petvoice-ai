# health_check.py
# Uygulama sağlık kontrolü
# Bu dosya, uygulamanın sağlık durumunu kontrol eder

import os
import sys
import importlib
from app import create_app, db
from app.models.models import User, Pet, SoundAnalysis

def check_python_version():
    """Python sürümünü kontrol eder"""
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print("✓ Python sürümü uygun: {}.{}.{}".format(version.major, version.minor, version.micro))
        return True
    else:
        print("✗ Python sürümü uygun değil: {}.{}.{}".format(version.major, version.minor, version.micro))
        return False

def check_required_packages():
    """Gerekli paketleri kontrol eder"""
    required_packages = [
        'flask',
        'flask_sqlalchemy',
        'flask_login',
        'google.generativeai',
        'librosa',
        'scipy',
        'numpy',
        'matplotlib',
        'celery',
        'redis'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            importlib.import_module(package)
            print(f"✓ {package} paketi yüklü")
        except ImportError:
            print(f"✗ {package} paketi yüklü değil")
            missing_packages.append(package)
    
    return len(missing_packages) == 0

def check_database_connection():
    """Veritabanı bağlantısını kontrol eder"""
    try:
        app = create_app(os.getenv('FLASK_CONFIG') or 'default')
        
        with app.app_context():
            # Basit bir sorgu çalıştır
            db.session.query(User).first()
            print("✓ Veritabanı bağlantısı başarılı")
            return True
    except Exception as e:
        print(f"✗ Veritabanı bağlantısı başarısız: {e}")
        return False

def check_ai_api():
    """AI API bağlantısını kontrol eder"""
    try:
        import google.generativeai as genai
        
        api_key = os.getenv('GOOGLE_API_KEY')
        if not api_key:
            print("✗ GOOGLE_API_KEY ortam değişkeni ayarlanmamış")
            return False
        
        genai.configure(api_key=api_key)
        models = genai.list_models()
        print("✓ Google AI API bağlantısı başarılı")
        return True
    except Exception as e:
        print(f"✗ Google AI API bağlantısı başarısız: {e}")
        return False

def check_redis_connection():
    """Redis bağlantısını kontrol eder"""
    try:
        import redis
        
        redis_url = os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/0')
        r = redis.from_url(redis_url)
        r.ping()
        print("✓ Redis bağlantısı başarılı")
        return True
    except Exception as e:
        print(f"✗ Redis bağlantısı başarısız: {e}")
        return False

def check_file_permissions():
    """Dosya izinlerini kontrol eder"""
    required_dirs = ['uploads', 'uploads/sounds', 'uploads/spectrograms']
    
    for directory in required_dirs:
        if not os.path.exists(directory):
            try:
                os.makedirs(directory)
                print(f"✓ {directory} dizini oluşturuldu")
            except Exception as e:
                print(f"✗ {directory} dizini oluşturulamadı: {e}")
                return False
        else:
            # Yazma izni kontrolü
            if os.access(directory, os.W_OK):
                print(f"✓ {directory} dizinine yazma izni var")
            else:
                print(f"✗ {directory} dizinine yazma izni yok")
                return False
    
    return True

def check_database_integrity():
    """Veritabanı bütünlüğünü kontrol eder"""
    try:
        app = create_app(os.getenv('FLASK_CONFIG') or 'default')
        
        with app.app_context():
            # Temel tabloların varlığını kontrol et
            tables = db.metadata.tables.keys()
            required_tables = ['users', 'pets', 'sound_analyses']
            
            for table in required_tables:
                if table in tables:
                    print(f"✓ {table} tablosu mevcut")
                else:
                    print(f"✗ {table} tablosu mevcut değil")
                    return False
            
            return True
    except Exception as e:
        print(f"✗ Veritabanı bütünlüğü kontrolü başarısız: {e}")
        return False

def main():
    """Ana fonksiyon"""
    print("PetVoice AI Sağlık Kontrolü")
    print("=" * 30)
    
    checks = [
        ("Python Sürümü", check_python_version),
        ("Gerekli Paketler", check_required_packages),
        ("Veritabanı Bağlantısı", check_database_connection),
        ("AI API Bağlantısı", check_ai_api),
        ("Redis Bağlantısı", check_redis_connection),
        ("Dosya İzinleri", check_file_permissions),
        ("Veritabanı Bütünlüğü", check_database_integrity)
    ]
    
    passed_checks = 0
    total_checks = len(checks)
    
    for check_name, check_function in checks:
        print(f"\n{check_name} Kontrolü:")
        if check_function():
            passed_checks += 1
        print()
    
    print("=" * 30)
    print(f"Sonuç: {passed_checks}/{total_checks} kontrol başarılı")
    
    if passed_checks == total_checks:
        print("✓ Uygulama sağlıklı görünüyor")
        return 0
    else:
        print("✗ Uygulamada bazı sorunlar var")
        return 1

if __name__ == '__main__':
    sys.exit(main())