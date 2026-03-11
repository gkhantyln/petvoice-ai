#!/usr/bin/env python3
# manage.py
# Uygulama yönetim aracı
# Bu dosya, uygulamayı yönetmek için çeşitli komutlar sağlar

import sys
import os
import subprocess
from datetime import datetime

def show_help():
    """Yardım mesajını gösterir"""
    help_text = """
PetVoice AI Yönetim Aracı

Kullanım:
  python manage.py <komut> [seçenekler]

Mevcut komutlar:
  help              Bu yardım mesajını gösterir
  run               Uygulamayı başlatır
  test              Testleri çalıştırır
  backup            Veritabanı yedeği alır
  restore <dosya>   Yedekten geri yükler
  clean             Eski dosyaları temizler
  health            Sağlık kontrolü yapar
  docs              API dökümantasyonu oluşturur
  monitor           Uygulama izleme başlatır
  init              Veritabanını başlatır
  shell             Etkileşimli shell başlatır
  celery            Celery worker'ı başlatır
  redis             Redis sunucusunu başlatır

Örnekler:
  python manage.py run
  python manage.py test
  python manage.py backup
  python manage.py health
"""
    print(help_text)

def run_app():
    """Uygulamayı başlatır"""
    print("Flask uygulaması başlatılıyor...")
    os.environ.setdefault('FLASK_APP', 'run.py')
    os.environ.setdefault('FLASK_ENV', 'development')
    
    subprocess.run([sys.executable, '-m', 'flask', 'run', '--host=0.0.0.0', '--port=5000'])

def run_tests():
    """Testleri çalıştırır"""
    print("Testler çalıştırılıyor...")
    subprocess.run([sys.executable, 'run_tests.py'])

def backup_db():
    """Veritabanı yedeği alır"""
    print("Veritabanı yedeği alınıyor...")
    subprocess.run([sys.executable, 'backup_db.py', 'backup'])

def restore_db(backup_file):
    """Yedekten geri yükler"""
    print(f"Yedekten geri yükleniyor: {backup_file}")
    subprocess.run([sys.executable, 'backup_db.py', 'restore', backup_file])

def clean_files():
    """Eski dosyaları temizler"""
    print("Eski dosyalar temizleniyor...")
    subprocess.run([sys.executable, 'cleanup.py'])

def health_check():
    """Sağlık kontrolü yapar"""
    print("Sağlık kontrolü yapılıyor...")
    subprocess.run([sys.executable, 'health_check.py'])

def generate_docs():
    """API dökümantasyonu oluşturur"""
    print("API dökümantasyonu oluşturuluyor...")
    subprocess.run([sys.executable, 'generate_docs.py'])

def start_monitor():
    """Uygulama izleme başlatır"""
    print("Uygulama izleme başlatılıyor...")
    subprocess.run([sys.executable, 'monitor.py'])

def init_database():
    """Veritabanını başlatır"""
    print("Veritabanı başlatılıyor...")
    subprocess.run([sys.executable, 'init_db.py'])

def start_shell():
    """Etkileşimli shell başlatır"""
    print("Etkileşimli shell başlatılıyor...")
    os.environ.setdefault('FLASK_APP', 'run.py')
    subprocess.run([sys.executable, '-m', 'flask', 'shell'])

def start_celery():
    """Celery worker'ı başlatır"""
    print("Celery worker başlatılıyor...")
    subprocess.run([
        'celery', '-A', 'app.celery_worker.celery', 'worker', '--loglevel=info'
    ])

def start_redis():
    """Redis sunucusunu başlatır"""
    print("Redis sunucusu başlatılıyor...")
    try:
        subprocess.run(['redis-server'])
    except FileNotFoundError:
        print("Redis sunucusu bulunamadı. Lütfen Redis'i yükleyin.")

def main():
    """Ana fonksiyon"""
    if len(sys.argv) < 2:
        show_help()
        return
    
    command = sys.argv[1]
    
    if command == 'help':
        show_help()
    elif command == 'run':
        run_app()
    elif command == 'test':
        run_tests()
    elif command == 'backup':
        backup_db()
    elif command == 'restore':
        if len(sys.argv) < 3:
            print("Yedek dosyası adı belirtilmelidir.")
            return
        restore_db(sys.argv[2])
    elif command == 'clean':
        clean_files()
    elif command == 'health':
        health_check()
    elif command == 'docs':
        generate_docs()
    elif command == 'monitor':
        start_monitor()
    elif command == 'init':
        init_database()
    elif command == 'shell':
        start_shell()
    elif command == 'celery':
        start_celery()
    elif command == 'redis':
        start_redis()
    else:
        print(f"Bilinmeyen komut: {command}")
        show_help()

if __name__ == '__main__':
    main()