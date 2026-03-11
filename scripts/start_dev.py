# start_dev.py
# Geliştirme ortamı başlatıcı
# Bu dosya, geliştirme ortamını başlatmak için kullanılır

import os
import subprocess
import sys
import time
from threading import Thread

def start_redis():
    """Redis sunucusunu başlatır"""
    try:
        print("Redis sunucusu başlatılıyor...")
        subprocess.Popen(['redis-server'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(2)  # Redis'in başlaması için bekle
        print("Redis sunucusu başlatıldı.")
    except FileNotFoundError:
        print("UYARI: Redis sunucusu bulunamadı. Arka plan görevleri çalışmayabilir.")
        print("Lütfen Redis'i yükleyin: https://redis.io/download/")

def start_celery():
    """Celery worker'ı başlatır"""
    try:
        print("Celery worker başlatılıyor...")
        subprocess.Popen([
            'celery', '-A', 'app.celery_worker.celery', 'worker', '--loglevel=info'
        ])
        print("Celery worker başlatıldı.")
    except FileNotFoundError:
        print("UYARI: Celery bulunamadı. Arka plan görevleri çalışmayabilir.")
        print("Lütfen 'pip install celery' komutunu çalıştırın.")

def start_flask():
    """Flask uygulamasını başlatır"""
    print("Flask uygulaması başlatılıyor...")
    os.environ['FLASK_APP'] = 'run.py'
    os.environ['FLASK_ENV'] = 'development'
    os.environ['FLASK_DEBUG'] = '1'
    
    subprocess.run(['flask', 'run', '--host=0.0.0.0', '--port=5000'])

def main():
    """Ana fonksiyon"""
    print("PetVoice AI Geliştirme Ortamı Başlatılıyor...")
    print("=" * 50)
    
    # Ortam değişkenlerini ayarla
    os.environ.setdefault('SECRET_KEY', 'gelistirme-icin-gizli-anahtar')
    os.environ.setdefault('DATABASE_URL', 'sqlite:///petvoice_dev.db')
    os.environ.setdefault('GOOGLE_API_KEY', 'YOUR_GOOGLE_API_KEY_HERE')
    os.environ.setdefault('CELERY_BROKER_URL', 'redis://localhost:6379/0')
    os.environ.setdefault('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')
    
    # Redis'i başlat
    redis_thread = Thread(target=start_redis)
    redis_thread.daemon = True
    redis_thread.start()
    
    # Celery'i başlat
    celery_thread = Thread(target=start_celery)
    celery_thread.daemon = True
    celery_thread.start()
    
    # Flask uygulamasını başlat
    try:
        start_flask()
    except KeyboardInterrupt:
        print("\nUygulama kapatılıyor...")
        sys.exit(0)
    except Exception as e:
        print(f"Hata oluştu: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()