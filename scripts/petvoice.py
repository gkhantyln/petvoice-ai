#!/usr/bin/env python3
# petvoice.py
# PetVoice AI Ana Yönetim Betiği
# Bu dosya, tüm yönetim işlemlerini tek bir yerden yönetir

import sys
import os
import subprocess
from pathlib import Path

def show_banner():
    """Banner gösterir"""
    banner = """
    ██████╗ ███████╗████████╗██╗   ██╗ ██████╗ ██████╗ ██╗███████╗
    ██╔══██╗██╔════╝╚══██╔══╝██║   ██║██╔═══██╗██╔══██╗██║██╔════╝
    ██████╔╝█████╗     ██║   ██║   ██║██║   ██║██████╔╝██║█████╗  
    ██╔═══╝ ██╔══╝     ██║   ██║   ██║██║   ██║██╔══██╗██║██╔══╝  
    ██║     ███████╗   ██║   ╚██████╔╝╚██████╔╝██║  ██║██║███████╗
    ╚═╝     ╚══════╝   ╚═╝    ╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚═╝╚══════╝
    
    █████╗ ██╗██╗   ██╗ █████╗ ███╗   ██╗ █████╗ ██╗     
    ██╔══██╗██║╚██╗ ██╔╝██╔══██╗████╗  ██║██╔══██╗██║     
    ███████║██║ ╚████╔╝ ███████║██╔██╗ ██║███████║██║     
    ██╔══██║██║  ╚██╔╝  ██╔══██║██║╚██╗██║██╔══██║██║     
    ██║  ██║██║   ██║   ██║  ██║██║ ╚████║██║  ██║███████╗
    ╚═╝  ╚═╝╚═╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚══════╝
    
    Hayvan Ses Analizi Platformu - Yönetim Aracı
    """
    print(banner)

def show_menu():
    """Ana menüyü gösterir"""
    menu = """
╔══════════════════════════════════════════════════════════════╗
║                   PetVoice AI Yönetim Menüsü                 ║
╠══════════════════════════════════════════════════════════════╣
║ 1. Uygulamayı Başlat          │ 2. Testleri Çalıştır         ║
║ 3. Sağlık Kontrolü            │ 4. Güvenlik Kontrolü         ║
║ 5. Veritabanı Yedeği Al       │ 6. Yedekten Geri Yükle       ║
║ 7. Dosya Temizleme            │ 8. Uygulama İzleme           ║
║ 9. API Dokümantasyonu         │ 10. Geliştirici Kurulumu     ║
║ 11. Veritabanı Başlat         │ 12. Ortam Değişkenleri Ayarla║
║ 13. Proje Özeti Oluştur       │ 14. Dağıtım Paketi Oluştur   ║
║ 15. Uygulama Güncelle         │ 0. Çıkış                     ║
╚══════════════════════════════════════════════════════════════╝
    """
    print(menu)

def get_choice():
    """Kullanıcı seçimini alır"""
    try:
        choice = input("Seçiminiz (0-15): ").strip()
        return int(choice)
    except ValueError:
        return -1

def run_script(script_name, args=None):
    """Betik çalıştırır"""
    if args is None:
        args = []
    
    script_path = Path(script_name)
    if not script_path.exists():
        print(f"❌ Betik bulunamadı: {script_name}")
        return False
    
    try:
        cmd = [sys.executable, str(script_path)] + args
        result = subprocess.run(cmd)
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Betik çalıştırılırken hata oluştu: {e}")
        return False

def setup_environment():
    """Ortam değişkenlerini ayarlar"""
    print("Ortam değişkenleri ayarlanıyor...")
    
    # Gerekli ortam değişkenleri
    env_vars = {
        'FLASK_APP': 'run.py',
        'FLASK_ENV': 'development',
        'SECRET_KEY': 'gelistirme-icin-gizli-anahtar'
    }
    
    for key, value in env_vars.items():
        os.environ[key] = value
        print(f"✓ {key} = {value}")
    
    print("✓ Ortam değişkenleri ayarlandı")

def main():
    """Ana fonksiyon"""
    show_banner()
    
    # Varsayılan ortam değişkenlerini ayarla
    setup_environment()
    
    while True:
        show_menu()
        choice = get_choice()
        
        if choice == 0:
            print("👋 Görüşmek üzere!")
            break
        elif choice == 1:
            print("🚀 Uygulama başlatılıyor...")
            run_script('run.py')
        elif choice == 2:
            print("🧪 Testler çalıştırılıyor...")
            run_script('run_tests.py')
        elif choice == 3:
            print("🩺 Sağlık kontrolü yapılıyor...")
            run_script('health_check.py')
        elif choice == 4:
            print("🔒 Güvenlik kontrolü yapılıyor...")
            run_script('security_check.py')
        elif choice == 5:
            print("💾 Veritabanı yedeği alınıyor...")
            run_script('backup_db.py', ['backup'])
        elif choice == 6:
            backup_file = input("Yedek dosya adı: ").strip()
            if backup_file:
                print(f"🔄 {backup_file} dosyasından geri yükleniyor...")
                run_script('backup_db.py', ['restore', backup_file])
        elif choice == 7:
            print("🧹 Dosya temizleme yapılıyor...")
            run_script('cleanup.py')
        elif choice == 8:
            print("📊 Uygulama izleme başlatılıyor...")
            run_script('monitor.py')
        elif choice == 9:
            print("📚 API dokümantasyonu oluşturuluyor...")
            run_script('generate_docs.py')
        elif choice == 10:
            print("🔧 Geliştirici kurulumu yapılıyor...")
            run_script('setup_dev.py')
        elif choice == 11:
            print("🗄️ Veritabanı başlatılıyor...")
            run_script('init_db.py')
        elif choice == 12:
            print("⚙️ Ortam değişkenleri ayarlanıyor...")
            # Basit bir ortam değişkeni ayarlama
            key = input("Değişken adı: ").strip()
            value = input("Değişken değeri: ").strip()
            if key and value:
                os.environ[key] = value
                print(f"✓ {key} = {value}")
        elif choice == 13:
            print("📋 Proje özeti oluşturuluyor...")
            run_script('project_summary.py')
        elif choice == 14:
            print("📦 Dağıtım paketi oluşturuluyor...")
            run_script('deploy.py')
        elif choice == 15:
            print("⬆️ Uygulama güncelleniyor...")
            run_script('update.py')
        else:
            print("❌ Geçersiz seçim. Lütfen 0-15 arasında bir sayı girin.")
        
        input("\nDevam etmek için Enter tuşuna basın...")

if __name__ == '__main__':
    main()