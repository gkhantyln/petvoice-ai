# app/celery_worker.py
# Celery worker yapılandırması
# Bu dosya, arka plan görevlerini işlemek için Celery worker'ı yapılandırır

# Tasks modülünü import et
from app.tasks import celery

if __name__ == '__main__':
    celery.start()
