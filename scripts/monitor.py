# monitor.py
# Uygulama izleme aracı
# Bu dosya, uygulamanın performansını ve durumunu izler

import psutil
import time
import os
from datetime import datetime
import sqlite3

def get_system_stats():
    """Sistem istatistiklerini alır"""
    # CPU kullanımı
    cpu_percent = psutil.cpu_percent(interval=1)
    
    # Bellek kullanımı
    memory = psutil.virtual_memory()
    memory_percent = memory.percent
    memory_used = memory.used / (1024**3)  # GB cinsinden
    memory_total = memory.total / (1024**3)  # GB cinsinden
    
    # Disk kullanımı
    disk = psutil.disk_usage('/')
    disk_percent = (disk.used / disk.total) * 100
    disk_used = disk.used / (1024**3)  # GB cinsinden
    disk_total = disk.total / (1024**3)  # GB cinsinden
    
    return {
        'cpu_percent': cpu_percent,
        'memory_percent': memory_percent,
        'memory_used': round(memory_used, 2),
        'memory_total': round(memory_total, 2),
        'disk_percent': round(disk_percent, 2),
        'disk_used': round(disk_used, 2),
        'disk_total': round(disk_total, 2)
    }

def get_process_stats():
    """Uygulama süreci istatistiklerini alır"""
    current_process = psutil.Process(os.getpid())
    
    # Bellek kullanımı
    memory_info = current_process.memory_info()
    memory_mb = memory_info.rss / (1024**2)  # MB cinsinden
    
    # CPU kullanımı
    cpu_percent = current_process.cpu_percent()
    
    # Açık dosya sayısı
    try:
        open_files = len(current_process.open_files())
    except:
        open_files = 0
    
    # Ağ bağlantıları
    try:
        connections = len(current_process.connections())
    except:
        connections = 0
    
    return {
        'pid': current_process.pid,
        'memory_mb': round(memory_mb, 2),
        'cpu_percent': cpu_percent,
        'open_files': open_files,
        'connections': connections,
        'status': current_process.status()
    }

def get_database_stats():
    """Veritabanı istatistiklerini alır"""
    try:
        # SQLite veritabanı için istatistikler
        db_path = 'petvoice_dev.db'  # Geliştirme veritabanı
        if not os.path.exists(db_path):
            db_path = os.environ.get('DATABASE_URL', '').replace('sqlite:///', '')
        
        if os.path.exists(db_path):
            db_size = os.path.getsize(db_path) / (1024**2)  # MB cinsinden
            
            # Tablo sayılarını al
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            table_count = len(tables)
            conn.close()
            
            return {
                'db_size_mb': round(db_size, 2),
                'table_count': table_count
            }
    except Exception as e:
        return {
            'error': str(e)
        }
    
    return {}

def log_stats(stats):
    """İstatistikleri log dosyasına yazar"""
    log_file = 'logs/monitor.log'
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    log_entry = f"[{timestamp}] "
    log_entry += f"CPU: {stats['system']['cpu_percent']}% | "
    log_entry += f"Memory: {stats['system']['memory_percent']}% | "
    log_entry += f"App Memory: {stats['process']['memory_mb']}MB | "
    log_entry += f"App CPU: {stats['process']['cpu_percent']}%\n"
    
    with open(log_file, 'a') as f:
        f.write(log_entry)

def display_stats(stats):
    """İstatistikleri ekranda gösterir"""
    # Ekranı temizle
    os.system('cls' if os.name == 'nt' else 'clear')
    
    print("=" * 60)
    print("🐾 PetVoice AI Uygulama İzleme")
    print("=" * 60)
    print(f"Son güncelleme: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Sistem istatistikleri
    print("🖥️  Sistem İstatistikleri")
    print("-" * 30)
    print(f"CPU Kullanımı     : {stats['system']['cpu_percent']}%")
    print(f"Bellek Kullanımı  : {stats['system']['memory_percent']}% ({stats['system']['memory_used']}GB / {stats['system']['memory_total']}GB)")
    print(f"Disk Kullanımı    : {stats['system']['disk_percent']}% ({stats['system']['disk_used']}GB / {stats['system']['disk_total']}GB)")
    print()
    
    # Uygulama istatistikleri
    print("🚀 Uygulama İstatistikleri")
    print("-" * 30)
    print(f"PID               : {stats['process']['pid']}")
    print(f"Bellek Kullanımı  : {stats['process']['memory_mb']} MB")
    print(f"CPU Kullanımı     : {stats['process']['cpu_percent']}%")
    print(f"Açık Dosyalar     : {stats['process']['open_files']}")
    print(f"Ağ Bağlantıları   : {stats['process']['connections']}")
    print(f"Süreç Durumu      : {stats['process']['status']}")
    print()
    
    # Veritabanı istatistikleri
    if 'db_size_mb' in stats['database']:
        print("🗄️  Veritabanı İstatistikleri")
        print("-" * 30)
        print(f"Veritabanı Boyutu : {stats['database']['db_size_mb']} MB")
        print(f"Tablo Sayısı      : {stats['database']['table_count']}")
        print()
    elif 'error' in stats['database']:
        print("❌ Veritabanı İstatistikleri")
        print("-" * 30)
        print(f"Hata: {stats['database']['error']}")
        print()
    
    print("💡 Komutlar: 'q' tuşu ile çıkış yapabilirsiniz")
    print("=" * 60)

def main():
    """Ana fonksiyon"""
    print("PetVoice AI Uygulama İzleme Başlatılıyor...")
    
    try:
        while True:
            # İstatistikleri topla
            stats = {
                'system': get_system_stats(),
                'process': get_process_stats(),
                'database': get_database_stats()
            }
            
            # Ekranda göster
            display_stats(stats)
            
            # Log dosyasına yaz
            log_stats(stats)
            
            # 5 saniye bekle veya 'q' tuşu ile çıkış
            print("Güncellemek için bekleniyor... (Çıkmak için 'q' tuşuna basın)")
            try:
                # Windows için input timeout
                import msvcrt
                for i in range(50):  # 5 saniye
                    if msvcrt.kbhit():
                        key = msvcrt.getch().decode('utf-8')
                        if key.lower() == 'q':
                            print("\nİzleme durduruldu.")
                            return
                    time.sleep(0.1)
            except ImportError:
                # Diğer sistemler için
                time.sleep(5)
                
    except KeyboardInterrupt:
        print("\n\nİzleme durduruldu.")
    except Exception as e:
        print(f"\nHata oluştu: {e}")

if __name__ == '__main__':
    main()