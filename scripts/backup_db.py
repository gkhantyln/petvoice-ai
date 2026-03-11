# backup_db.py
# Veritabanı yedekleme aracı
# Bu dosya, veritabanının yedeğini almak için kullanılır

import os
import sys
import shutil
from datetime import datetime
from app import create_app, db

def backup_database():
    """Veritabanının yedeğini alır"""
    app = create_app(os.getenv('FLASK_CONFIG') or 'default')
    
    with app.app_context():
        # Yedekleme dizinini oluştur
        backup_dir = 'backups'
        os.makedirs(backup_dir, exist_ok=True)
        
        # Veritabanı dosyasının yolunu al
        db_uri = app.config['SQLALCHEMY_DATABASE_URI']
        
        if db_uri.startswith('sqlite:///'):
            # SQLite veritabanı
            db_path = db_uri.replace('sqlite:///', '')
            if os.path.exists(db_path):
                # Yedek dosya adını oluştur
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                backup_filename = f"petvoice_backup_{timestamp}.db"
                backup_path = os.path.join(backup_dir, backup_filename)
                
                # Dosyayı kopyala
                shutil.copy2(db_path, backup_path)
                print(f"Veritabanı yedeği oluşturuldu: {backup_path}")
            else:
                print(f"Veritabanı dosyası bulunamadı: {db_path}")
        else:
            # Diğer veritabanları için pg_dump veya benzeri araçlar kullanılmalı
            print("Bu betik sadece SQLite veritabanları için yedekleme yapabilir.")
            print("PostgreSQL için 'pg_dump' komutunu kullanın.")
            print("MySQL için 'mysqldump' komutunu kullanın.")

def list_backups():
    """Mevcut yedekleri listeler"""
    backup_dir = 'backups'
    if os.path.exists(backup_dir):
        backups = os.listdir(backup_dir)
        if backups:
            print("Mevcut yedekler:")
            for backup in sorted(backups):
                print(f"  - {backup}")
        else:
            print("Yedek bulunamadı.")
    else:
        print("Yedekleme dizini bulunamadı.")

def restore_backup(backup_filename):
    """Yedekten geri yükler"""
    backup_dir = 'backups'
    backup_path = os.path.join(backup_dir, backup_filename)
    
    if os.path.exists(backup_path):
        # Uygulamayı başlat
        app = create_app(os.getenv('FLASK_CONFIG') or 'default')
        
        with app.app_context():
            db_uri = app.config['SQLALCHEMY_DATABASE_URI']
            
            if db_uri.startswith('sqlite:///'):
                db_path = db_uri.replace('sqlite:///', '')
                
                # Veritabanı dosyasını yedekle
                if os.path.exists(db_path):
                    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                    old_backup = f"{db_path}.old_{timestamp}"
                    shutil.copy2(db_path, old_backup)
                    print(f"Mevcut veritabanı yedeklendi: {old_backup}")
                
                # Yedekten geri yükle
                shutil.copy2(backup_path, db_path)
                print(f"Veritabanı geri yüklendi: {backup_path}")
            else:
                print("Bu betik sadece SQLite veritabanları için geri yükleme yapabilir.")
    else:
        print(f"Yedek dosyası bulunamadı: {backup_path}")

def main():
    """Ana fonksiyon"""
    if len(sys.argv) < 2:
        print("Kullanım:")
        print("  python backup_db.py backup     - Veritabanı yedeği al")
        print("  python backup_db.py list       - Yedekleri listele")
        print("  python backup_db.py restore <dosya> - Yedekten geri yükle")
        return
    
    command = sys.argv[1]
    
    if command == 'backup':
        backup_database()
    elif command == 'list':
        list_backups()
    elif command == 'restore':
        if len(sys.argv) < 3:
            print("Yedek dosyası adı belirtilmelidir.")
            return
        restore_backup(sys.argv[2])
    else:
        print(f"Bilinmeyen komut: {command}")
        print("Kullanılabilir komutlar: backup, list, restore")

if __name__ == '__main__':
    main()