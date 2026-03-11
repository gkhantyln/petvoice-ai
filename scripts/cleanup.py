# cleanup.py
# Dosya temizleme aracı
# Bu dosya, eski ve gereksiz dosyaları temizlemek için kullanılır

import os
import shutil
from datetime import datetime, timedelta

def clean_uploads():
    """Uploads dizinindeki eski dosyaları temizler"""
    uploads_dir = 'uploads'
    
    if not os.path.exists(uploads_dir):
        print(f"Uploads dizini bulunamadı: {uploads_dir}")
        return
    
    # 30 günden eski dosyaları sil
    cutoff_date = datetime.now() - timedelta(days=30)
    
    deleted_count = 0
    
    for root, dirs, files in os.walk(uploads_dir):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                # Dosya değiştirilme tarihini al
                mod_time = datetime.fromtimestamp(os.path.getmtime(file_path))
                
                # Dosya 30 günden eskiyse sil
                if mod_time < cutoff_date:
                    os.remove(file_path)
                    print(f"Silindi: {file_path}")
                    deleted_count += 1
            except Exception as e:
                print(f"Dosya silinirken hata oluştu {file_path}: {e}")
    
    print(f"Toplam {deleted_count} dosya silindi.")

def clean_temp_files():
    """Geçici dosyaları temizler"""
    temp_dirs = ['temp', 'tmp']
    
    for temp_dir in temp_dirs:
        if os.path.exists(temp_dir):
            try:
                shutil.rmtree(temp_dir)
                print(f"Geçici dizin temizlendi: {temp_dir}")
            except Exception as e:
                print(f"Geçici dizin temizlenirken hata oluştu {temp_dir}: {e}")

def clean_logs():
    """Log dosyalarını temizler"""
    log_extensions = ['.log']
    
    for root, dirs, files in os.walk('.'):
        for file in files:
            if any(file.endswith(ext) for ext in log_extensions):
                file_path = os.path.join(root, file)
                try:
                    # 7 günden eski log dosyalarını sil
                    mod_time = datetime.fromtimestamp(os.path.getmtime(file_path))
                    cutoff_date = datetime.now() - timedelta(days=7)
                    
                    if mod_time < cutoff_date:
                        os.remove(file_path)
                        print(f"Log dosyası silindi: {file_path}")
                except Exception as e:
                    print(f"Log dosyası silinirken hata oluştu {file_path}: {e}")

def main():
    """Ana fonksiyon"""
    print("Dosya temizleme işlemi başlatılıyor...")
    
    clean_uploads()
    clean_temp_files()
    clean_logs()
    
    print("Dosya temizleme işlemi tamamlandı.")

if __name__ == '__main__':
    main()