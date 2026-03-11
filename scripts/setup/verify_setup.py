#!/usr/bin/env python3
# verify_setup.py
# Kurulum doğrulama betiği
# Bu dosya, geliştirme ortamının doğru şekilde kurulduğunu doğrular

import os
import sys
import importlib
from pathlib import Path

def check_python_version():
    """Python sürümünü kontrol eder"""
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"✓ Python sürümü uygun: {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"✗ Python sürümü uygun değil: {version.major}.{version.minor}.{version.micro}")
        return False

def check_required_files():
    """Gerekli dosyaları kontrol eder"""
    required_files = [
        "run.py",
        "requirements.txt",
        "config.py",
        "README.md",
        "USAGE.md"
    ]
    
    missing_files = []
    
    for file in required_files:
        if not Path(file).exists():
            print(f"✗ Gerekli dosya eksik: {file}")
            missing_files.append(file)
        else:
            print(f"✓ {file} dosyası mevcut")
    
    return len(missing_files) == 0

def check_required_directories():
    """Gerekli dizinleri kontrol eder"""
    required_dirs = [
        "app",
        "app/models",
        "app/views",
        "app/templates",
        "app/static",
        "app/utils",
        "migrations",
        "tests"
    ]
    
    missing_dirs = []
    
    for directory in required_dirs:
        if not Path(directory).exists():
            print(f"✗ Gerekli dizin eksik: {directory}")
            missing_dirs.append(directory)
        else:
            print(f"✓ {directory} dizini mevcut")
    
    return len(missing_dirs) == 0

def check_python_packages():
    """Python paketlerini kontrol eder"""
    required_packages = [
        "flask",
        "flask_sqlalchemy",
        "flask_login",
        "flask_migrate",
        "flask_wtf",
        "google.generativeai",
        "librosa",
        "scipy",
        "numpy",
        "matplotlib",
        "pandas",
        "celery",
        "redis",
        "psycopg2"
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

def check_environment_variables():
    """Ortam değişkenlerini kontrol eder"""
    required_vars = [
        "SECRET_KEY"
    ]
    
    missing_vars = []
    
    for var in required_vars:
        if not os.environ.get(var):
            print(f"⚠️  {var} ortam değişkeni ayarlanmamış (zorunlu değil)")
            missing_vars.append(var)
        else:
            print(f"✓ {var} ortam değişkeni ayarlanmış")
    
    # API anahtarları (zorunlu değil ama önerilir)
    optional_vars = [
        "GOOGLE_API_KEY",
        "DATABASE_URL"
    ]
    
    for var in optional_vars:
        if not os.environ.get(var):
            print(f"⚠️  {var} ortam değişkeni ayarlanmamış (isteğe bağlı)")
        else:
            print(f"✓ {var} ortam değişkeni ayarlanmış")
    
    return True

def check_database():
    """Veritabanı bağlantısını kontrol eder"""
    try:
        # Basit bir veritabanı dosyası kontrolü
        db_files = ["petvoice_dev.db"]
        
        db_exists = False
        for db_file in db_files:
            if Path(db_file).exists():
                print(f"✓ Veritabanı dosyası mevcut: {db_file}")
                db_exists = True
                break
        
        if not db_exists:
            print("⚠️  Veritabanı dosyası bulunamadı (ilk kurulum için normal)")
        
        return True
    except Exception as e:
        print(f"✗ Veritabanı kontrolü sırasında hata oluştu: {e}")
        return False

def check_executable_scripts():
    """Çalıştırılabilir betikleri kontrol eder"""
    scripts = [
        "manage.py",
        "petvoice.py"
    ]
    
    for script in scripts:
        if Path(script).exists():
            print(f"✓ {script} betiği mevcut")
        else:
            print(f"✗ {script} betiği bulunamadı")
    
    return True

def main():
    """Ana fonksiyon"""
    print("PetVoice AI Kurulum Doğrulama")
    print("=" * 30)
    
    checks = [
        ("Python Sürümü", check_python_version),
        ("Gerekli Dosyalar", check_required_files),
        ("Gerekli Dizinler", check_required_directories),
        ("Python Paketleri", check_python_packages),
        ("Ortam Değişkenleri", check_environment_variables),
        ("Veritabanı", check_database),
        ("Çalıştırılabilir Betikler", check_executable_scripts)
    ]
    
    results = []
    
    for check_name, check_function in checks:
        print(f"\n{check_name} Kontrolü:")
        result = check_function()
        results.append(result)
        print()
    
    passed = sum(1 for result in results if result)
    total = len(results)
    
    print("=" * 30)
    print(f"Sonuç: {passed}/{total} kontrol başarılı")
    
    if passed == total:
        print("✅ Kurulum doğru şekilde tamamlanmış görünüyor")
        print("\n💡 Sonraki adımlar:")
        print("  - python manage.py run (uygulamayı başlatmak için)")
        print("  - python manage.py test (testleri çalıştırmak için)")
        print("  - python manage.py help (tüm komutları görmek için)")
        return 0
    else:
        print("⚠️  Kurulumda bazı eksiklikler var")
        print("Lütfen yukarıdaki hataları kontrol edin ve gerekli düzeltmeleri yapın")
        return 1

if __name__ == '__main__':
    sys.exit(main())