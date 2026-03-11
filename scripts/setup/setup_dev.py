#!/usr/bin/env python3
# setup_dev.py
# Geliştirici kurulum betiği
# Bu dosya, yeni geliştiriciler için ortam kurulumunu kolaylaştırır

import os
import sys
import subprocess
import venv
from pathlib import Path

def check_python_version():
    """Python sürümünü kontrol eder"""
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"✓ Python sürümü uygun: {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"✗ Python sürümü uygun değil: {version.major}.{version.minor}.{version.micro}")
        print("Lütfen Python 3.8 veya üzeri bir sürüm yükleyin.")
        return False

def create_virtual_environment():
    """Sanal ortam oluşturur"""
    venv_path = Path("venv")
    
    if venv_path.exists():
        print("✓ Sanal ortam zaten mevcut")
        return True
    
    print("Sanal ortam oluşturuluyor...")
    try:
        venv.create(venv_path, with_pip=True)
        print("✓ Sanal ortam oluşturuldu")
        return True
    except Exception as e:
        print(f"✗ Sanal ortam oluşturulurken hata oluştu: {e}")
        return False

def install_requirements():
    """Gerekli paketleri yükler"""
    requirements_file = Path("requirements.txt")
    
    if not requirements_file.exists():
        print("✗ requirements.txt dosyası bulunamadı")
        return False
    
    print("Gerekli paketler yükleniyor...")
    try:
        # Sanal ortamın Python yolunu belirle
        if os.name == 'nt':  # Windows
            python_path = "venv\\Scripts\\python.exe"
        else:  # Unix/Linux/macOS
            python_path = "venv/bin/python"
        
        subprocess.run([python_path, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
        print("✓ Gerekli paketler yüklendi")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Paket yüklenirken hata oluştu: {e}")
        return False
    except Exception as e:
        print(f"✗ Beklenmeyen hata oluştu: {e}")
        return False

def setup_environment_variables():
    """Ortam değişkenlerini ayarlar"""
    env_file = Path(".env")
    
    if env_file.exists():
        print("✓ Ortam değişkenleri dosyası zaten mevcut")
        return True
    
    print("Ortam değişkenleri dosyası oluşturuluyor...")
    
    env_content = """# PetVoice AI Geliştirme Ortamı Değişkenleri
SECRET_KEY=gelistirme_icin_gizli_anahtar
DATABASE_URL=sqlite:///petvoice_dev.db
GOOGLE_API_KEY=google_gemini_api_anahtarınız
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0

# Flask ayarları
FLASK_APP=run.py
FLASK_ENV=development
FLASK_DEBUG=1
"""
    
    try:
        with open(env_file, "w") as f:
            f.write(env_content)
        print("✓ Ortam değişkenleri dosyası oluşturuldu")
        print("⚠️  Lütfen .env dosyasındaki GOOGLE_API_KEY değerini gerçek bir API anahtarı ile değiştirin")
        return True
    except Exception as e:
        print(f"✗ Ortam değişkenleri dosyası oluşturulurken hata oluştu: {e}")
        return False

def initialize_database():
    """Veritabanını başlatır"""
    print("Veritabanı başlatılıyor...")
    try:
        # Sanal ortamın Python yolunu belirle
        if os.name == 'nt':  # Windows
            python_path = "venv\\Scripts\\python.exe"
        else:  # Unix/Linux/macOS
            python_path = "venv/bin/python"
        
        subprocess.run([python_path, "init_db.py"], check=True)
        print("✓ Veritabanı başlatıldı")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Veritabanı başlatılırken hata oluştu: {e}")
        return False
    except Exception as e:
        print(f"✗ Beklenmeyen hata oluştu: {e}")
        return False

def create_directories():
    """Gerekli dizinleri oluşturur"""
    directories = [
        "uploads",
        "uploads/sounds",
        "uploads/spectrograms",
        "logs",
        "backups",
        "temp"
    ]
    
    print("Gerekli dizinler oluşturuluyor...")
    
    for directory in directories:
        try:
            os.makedirs(directory, exist_ok=True)
            print(f"✓ {directory} dizini oluşturuldu")
        except Exception as e:
            print(f"✗ {directory} dizini oluşturulurken hata oluştu: {e}")
            return False
    
    return True

def show_completion_message():
    """Tamamlanma mesajını gösterir"""
    print("\n" + "="*60)
    print("🎉 Geliştirme Ortamı Kurulumu Tamamlandı!")
    print("="*60)
    print("Şimdi yapmanız gerekenler:")
    print()
    print("1. Google Gemini API anahtarınızı alın:")
    print("   https://ai.google.dev/")
    print()
    print("2. .env dosyasındaki GOOGLE_API_KEY değerini güncelleyin")
    print()
    print("3. Redis sunucusunu başlatın:")
    print("   redis-server")
    print()
    print("4. Yeni bir terminal penceresinde Celery worker'ı başlatın:")
    print("   python manage.py celery")
    print()
    print("5. Ana terminalde uygulamayı başlatın:")
    print("   python manage.py run")
    print()
    print("6. Tarayıcınızda http://localhost:5000 adresine gidin")
    print()
    print("💡 Yardım için:")
    print("   python manage.py help")
    print("="*60)

def main():
    """Ana fonksiyon"""
    print("PetVoice AI Geliştirici Kurulumu")
    print("="*40)
    
    # Kontroller
    if not check_python_version():
        return
    
    # Kurulum adımları
    steps = [
        ("Sanal Ortam", create_virtual_environment),
        ("Dizinler", create_directories),
        ("Ortam Değişkenleri", setup_environment_variables),
        ("Paketler", install_requirements),
        ("Veritabanı", initialize_database)
    ]
    
    failed_steps = []
    
    for step_name, step_function in steps:
        print(f"\n{step_name} kurulumu yapılıyor...")
        if not step_function():
            failed_steps.append(step_name)
    
    # Sonuç
    if failed_steps:
        print(f"\n✗ Aşağıdaki adımlarda hata oluştu: {', '.join(failed_steps)}")
        print("Lütfen hataları kontrol edin ve tekrar deneyin.")
        return 1
    else:
        show_completion_message()
        return 0

if __name__ == '__main__':
    sys.exit(main())