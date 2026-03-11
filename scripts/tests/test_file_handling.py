# test_file_handling.py
# Dosya işleme testi
# Bu dosya, upload dizinlerinin doğru çalışıp çalışmadığını test eder

import os
from app import create_app

def test_file_handling():
    """Dosya işleme testi"""
    # Uygulamayı oluştur
    app = create_app('default')
    
    with app.app_context():
        # Upload klasörünü al
        upload_folder = app.config['UPLOAD_FOLDER']
        
        # Upload klasörünün tam yolunu al
        upload_folder = os.path.abspath(upload_folder)
        
        # Gerekli alt dizinleri kontrol et
        sounds_dir = os.path.join(upload_folder, 'sounds')
        spectrograms_dir = os.path.join(upload_folder, 'spectrograms')
        
        # Windows uyumluluğu için tam yolları kullan
        sounds_dir = os.path.abspath(sounds_dir)
        spectrograms_dir = os.path.abspath(spectrograms_dir)
        
        print(f"Upload klasörü: {upload_folder}")
        print(f"Ses dosyaları dizini: {sounds_dir}")
        print(f"Spektrogramlar dizini: {spectrograms_dir}")
        
        # Dizinlerin var olduğunu kontrol et
        if os.path.exists(sounds_dir):
            print("✓ Ses dosyaları dizini mevcut")
        else:
            print("✗ Ses dosyaları dizini bulunamadı")
            
        if os.path.exists(spectrograms_dir):
            print("✓ Spektrogramlar dizini mevcut")
        else:
            print("✗ Spektrogramlar dizini bulunamadı")
        
        # Dizinlerde dosya oluşturma testi
        try:
            test_file_path = os.path.join(sounds_dir, 'test.txt')
            with open(test_file_path, 'w') as f:
                f.write('Test dosyası')
            
            if os.path.exists(test_file_path):
                print("✓ Dosya oluşturma başarılı")
                # Test dosyasını sil
                os.remove(test_file_path)
            else:
                print("✗ Dosya oluşturma başarısız")
                
        except Exception as e:
            print(f"✗ Dosya oluşturma hatası: {e}")

if __name__ == '__main__':
    test_file_handling()