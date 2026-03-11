#!/usr/bin/env python3
# deploy.py
# Uygulama dağıtım betiği
# Bu dosya, uygulamayı üretim ortamına dağıtmak için kullanılır

import os
import sys
import subprocess
import shutil
from datetime import datetime
from pathlib import Path

def check_environment():
    """Dağıtım ortamını kontrol eder"""
    print("Dağıtım ortamı kontrol ediliyor...")
    
    # Python sürümünü kontrol et
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"✗ Python sürümü uygun değil: {version.major}.{version.minor}.{version.micro}")
        print("Lütfen Python 3.8 veya üzeri bir sürüm kullanın.")
        return False
    
    print(f"✓ Python sürümü uygun: {version.major}.{version.minor}.{version.micro}")
    return True

def create_deployment_package():
    """Dağıtım paketi oluşturur"""
    print("Dağıtım paketi oluşturuluyor...")
    
    # Dağıtım dizinini oluştur
    deploy_dir = Path("deployment")
    if deploy_dir.exists():
        shutil.rmtree(deploy_dir)
    
    deploy_dir.mkdir()
    
    # Gerekli dosya ve dizinleri kopyala
    required_items = [
        "app",
        "migrations",
        "config.py",
        "run.py",
        "requirements.txt",
        "README.md",
        "USAGE.md"
    ]
    
    for item in required_items:
        item_path = Path(item)
        if item_path.exists():
            if item_path.is_dir():
                shutil.copytree(item_path, deploy_dir / item)
            else:
                shutil.copy2(item_path, deploy_dir / item)
            print(f"✓ {item} kopyalandı")
        else:
            print(f"⚠️  {item} bulunamadı")
    
    # Dağıtım betiklerini kopyala
    deploy_scripts = [
        "init_db.py",
        "manage.py"
    ]
    
    for script in deploy_scripts:
        script_path = Path(script)
        if script_path.exists():
            shutil.copy2(script_path, deploy_dir / script)
            print(f"✓ {script} kopyalandı")
    
    print(f"✓ Dağıtım paketi oluşturuldu: {deploy_dir}")
    return True

def generate_deployment_config():
    """Dağıtım yapılandırması oluşturur"""
    print("Dağıtım yapılandırması oluşturuluyor...")
    
    deploy_dir = Path("deployment")
    
    # production.py yapılandırma dosyası
    config_content = """# production.py
# Üretim ortamı yapılandırması

import os

class ProductionConfig:
    \"""Üretim ortamı yapılandırması\"""
    
    # Gizli anahtar
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'uretim-icin-guvenli-bir-anahtar'
    
    # Veritabanı
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \\
        'postgresql://kullanici:sifre@localhost/petvoice'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Dosya yükleme
    UPLOAD_FOLDER = '/var/www/petvoice/uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    
    # AI API
    GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')
    
    # Celery
    CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL') or 'redis://localhost:6379/0'
    CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND') or 'redis://localhost:6379/0'
    
    # Güvenlik
    DEBUG = False
    TESTING = False

config = {
    'production': ProductionConfig
}
"""
    
    config_file = deploy_dir / "production.py"
    with open(config_file, "w") as f:
        f.write(config_content)
    
    print("✓ Üretim yapılandırması oluşturuldu")
    
    # systemd servis dosyası
    service_content = """[Unit]
Description=PetVoice AI Web Application
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/var/www/petvoice
Environment=FLASK_APP=run.py
Environment=FLASK_ENV=production
ExecStart=/var/www/petvoice/venv/bin/gunicorn -w 4 -b 0.0.0.0:5000 run:app
Restart=always

[Install]
WantedBy=multi-user.target
"""
    
    service_file = deploy_dir / "petvoice.service"
    with open(service_file, "w") as f:
        f.write(service_content)
    
    print("✓ systemd servis dosyası oluşturuldu")
    
    # nginx yapılandırması
    nginx_content = """server {
    listen 80;
    server_name petvoice.example.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static {
        alias /var/www/petvoice/app/static;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    client_max_body_size 16M;
}
"""
    
    nginx_file = deploy_dir / "petvoice.nginx"
    with open(nginx_file, "w") as f:
        f.write(nginx_content)
    
    print("✓ nginx yapılandırması oluşturuldu")
    
    return True

def create_install_script():
    """Kurulum betiği oluşturur"""
    print("Kurulum betiği oluşturuluyor...")
    
    deploy_dir = Path("deployment")
    
    install_content = """#!/bin/bash
# PetVoice AI Kurulum Betiği

set -e

echo "PetVoice AI Kurulumu Başlatılıyor..."

# Gerekli paketleri yükle
echo "Gerekli paketler yükleniyor..."
sudo apt-get update
sudo apt-get install -y python3 python3-pip python3-venv nginx redis-server postgresql

# Uygulama dizinini oluştur
echo "Uygulama dizini oluşturuluyor..."
sudo mkdir -p /var/www/petvoice
sudo chown www-data:www-data /var/www/petvoice

# Uygulama dosyalarını kopyala
echo "Uygulama dosyaları kopyalanıyor..."
sudo cp -r * /var/www/petvoice/
sudo chown -R www-data:www-data /var/www/petvoice

# Sanal ortam oluştur ve paketleri yükle
echo "Sanal ortam oluşturuluyor..."
cd /var/www/petvoice
sudo -u www-data python3 -m venv venv
sudo -u www-data /var/www/petvoice/venv/bin/pip install -r requirements.txt

# Veritabanı başlat
echo "Veritabanı başlatılıyor..."
sudo -u www-data /var/www/petvoice/venv/bin/python init_db.py

# nginx yapılandırması
echo "nginx yapılandırılıyor..."
sudo cp petvoice.nginx /etc/nginx/sites-available/petvoice
sudo ln -sf /etc/nginx/sites-available/petvoice /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl reload nginx

# systemd servisini kur
echo "systemd servisi kuruluyor..."
sudo cp petvoice.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable petvoice
sudo systemctl start petvoice

# Redis başlat
echo "Redis başlatılıyor..."
sudo systemctl enable redis-server
sudo systemctl start redis-server

echo "Kurulum tamamlandı!"
echo "Lütfen aşağıdaki ortam değişkenlerini ayarlayın:"
echo "  - SECRET_KEY"
echo "  - DATABASE_URL"
echo "  - GOOGLE_API_KEY"
echo "  - CELERY_BROKER_URL"
echo "  - CELERY_RESULT_BACKEND"
"""
    
    install_file = deploy_dir / "install.sh"
    with open(install_file, "w") as f:
        f.write(install_content)
    
    # Çalıştırma izni ver
    os.chmod(install_file, 0o755)
    
    print("✓ Kurulum betiği oluşturuldu")
    return True

def create_backup_script():
    """Yedekleme betiği oluşturur"""
    print("Yedekleme betiği oluşturuluyor...")
    
    deploy_dir = Path("deployment")
    
    backup_content = """#!/bin/bash
# PetVoice AI Yedekleme Betiği

BACKUP_DIR="/var/backups/petvoice"
DATE=$(date +%Y%m%d_%H%M%S)

# Yedekleme dizinini oluştur
mkdir -p $BACKUP_DIR

# Veritabanı yedeği
pg_dump petvoice > $BACKUP_DIR/petvoice_db_$DATE.sql

# Dosya yedeği
tar -czf $BACKUP_DIR/petvoice_files_$DATE.tar.gz /var/www/petvoice/uploads

# Eski yedekleri temizle (7 günden eski)
find $BACKUP_DIR -name "petvoice_*" -mtime +7 -delete

echo "Yedekleme tamamlandı: $BACKUP_DIR/petvoice_*_$DATE.*"
"""
    
    backup_file = deploy_dir / "backup.sh"
    with open(backup_file, "w") as f:
        f.write(backup_content)
    
    # Çalıştırma izni ver
    os.chmod(backup_file, 0o755)
    
    print("✓ Yedekleme betiği oluşturuldu")
    return True

def show_deployment_instructions():
    """Dağıtım talimatlarını gösterir"""
    print("\n" + "="*60)
    print("📦 Dağıtım Paketi Oluşturuldu!")
    print("="*60)
    print("Dağıtım paketi: deployment/")
    print()
    print("Dağıtım için yapmanız gerekenler:")
    print()
    print("1. deployment/ dizinini üretim sunucusuna kopyalayın")
    print()
    print("2. Üretim sunucusunda şu komutları çalıştırın:")
    print("   cd deployment")
    print("   chmod +x install.sh")
    print("   sudo ./install.sh")
    print()
    print("3. Ortam değişkenlerini ayarlayın:")
    print("   sudo nano /etc/systemd/system/petvoice.service")
    print("   Environment=SECRET_KEY=gercek_gizli_anahtar")
    print("   Environment=GOOGLE_API_KEY=google_api_anahtari")
    print("   ...")
    print()
    print("4. Servisleri yeniden başlatın:")
    print("   sudo systemctl daemon-reload")
    print("   sudo systemctl restart petvoice")
    print()
    print("5. Güvenlik için firewall yapılandırması yapın:")
    print("   sudo ufw allow 'Nginx Full'")
    print("="*60)

def main():
    """Ana fonksiyon"""
    print("PetVoice AI Dağıtım Betiği")
    print("="*30)
    
    # Ortam kontrolü
    if not check_environment():
        return 1
    
    # Dağıtım paketi oluşturma adımları
    steps = [
        ("Dağıtım Paketi", create_deployment_package),
        ("Yapılandırma", generate_deployment_config),
        ("Kurulum Betiği", create_install_script),
        ("Yedekleme Betiği", create_backup_script)
    ]
    
    failed_steps = []
    
    for step_name, step_function in steps:
        print(f"\n{step_name} oluşturuluyor...")
        if not step_function():
            failed_steps.append(step_name)
    
    # Sonuç
    if failed_steps:
        print(f"\n✗ Aşağıdaki adımlarda hata oluştu: {', '.join(failed_steps)}")
        print("Lütfen hataları kontrol edin ve tekrar deneyin.")
        return 1
    else:
        show_deployment_instructions()
        return 0

if __name__ == '__main__':
    sys.exit(main())