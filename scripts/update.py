#!/usr/bin/env python3
# update.py
# Uygulama güncelleme betiği
# Bu dosya, uygulamayı yeni sürümlere güncellemek için kullanılır

import os
import sys
import subprocess
import shutil
from datetime import datetime
from pathlib import Path

def check_current_version():
    """Mevcut sürümü kontrol eder"""
    print("Mevcut sürüm kontrol ediliyor...")
    
    # Version dosyası kontrolü (varsa)
    version_file = Path("VERSION")
    if version_file.exists():
        with open(version_file, "r") as f:
            current_version = f.read().strip()
        print(f"✓ Mevcut sürüm: {current_version}")
    else:
        print("✓ Sürüm dosyası bulunamadı, ilk kurulum gibi davranılıyor")
        current_version = "0.0.0"
    
    return current_version

def backup_current_version():
    """Mevcut sürümü yedekler"""
    print("Mevcut sürüm yedekleniyor...")
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_name = f"petvoice_backup_{timestamp}"
    
    try:
        # Veritabanı yedeği
        subprocess.run([sys.executable, "backup_db.py", "backup"], check=True)
        
        # Dosya yedeği
        backup_dir = Path("backups") / backup_name
        backup_dir.mkdir(parents=True, exist_ok=True)
        
        # Önemli dosya ve dizinleri yedekle
        important_items = [
            "app",
            "config.py",
            "uploads"
        ]
        
        for item in important_items:
            item_path = Path(item)
            if item_path.exists():
                if item_path.is_dir():
                    shutil.copytree(item_path, backup_dir / item)
                else:
                    shutil.copy2(item_path, backup_dir / item)
                print(f"✓ {item} yedeklendi")
        
        print(f"✓ Yedekleme tamamlandı: {backup_dir}")
        return True
    except Exception as e:
        print(f"✗ Yedekleme sırasında hata oluştu: {e}")
        return False

def pull_latest_changes():
    """En son değişiklikleri çeker"""
    print("En son değişiklikler alınıyor...")
    
    try:
        # Git kontrolü
        result = subprocess.run(["git", "status"], capture_output=True, text=True)
        if result.returncode != 0:
            print("✗ Git deposu bulunamadı. Manuel güncelleme gerekiyor.")
            return False
        
        # En son değişiklikleri çek
        subprocess.run(["git", "pull"], check=True)
        print("✓ En son değişiklikler alındı")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Değişiklikler alınırken hata oluştu: {e}")
        return False
    except FileNotFoundError:
        print("✗ Git bulunamadı. Lütfen Git'i yükleyin.")
        return False

def update_dependencies():
    """Bağımlılıkları günceller"""
    print("Bağımlılıklar güncelleniyor...")
    
    try:
        # requirements.txt kontrolü
        requirements_file = Path("requirements.txt")
        if not requirements_file.exists():
            print("⚠️  requirements.txt dosyası bulunamadı")
            return True
        
        # Pip güncellemesi
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt", "--upgrade"], check=True)
        print("✓ Bağımlılıklar güncellendi")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Bağımlılıklar güncellenirken hata oluştu: {e}")
        return False

def run_migrations():
    """Veritabanı migration'larını çalıştırır"""
    print("Veritabanı migration'ları çalıştırılıyor...")
    
    try:
        # Flask-Migrate kontrolü
        import flask_migrate
        print("✓ Flask-Migrate mevcut")
        
        # Migration'ları çalıştır
        os.environ.setdefault('FLASK_APP', 'run.py')
        subprocess.run([sys.executable, "-m", "flask", "db", "upgrade"], check=True)
        print("✓ Veritabanı migration'ları tamamlandı")
        return True
    except ImportError:
        print("⚠️  Flask-Migrate bulunamadı, migration atlanıyor")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Migration sırasında hata oluştu: {e}")
        return False
    except Exception as e:
        print(f"✗ Beklenmeyen hata oluştu: {e}")
        return False

def restart_services():
    """Servisleri yeniden başlatır"""
    print("Servisler yeniden başlatılıyor...")
    
    try:
        # Sistem kontrolü
        if os.name == 'nt':  # Windows
            print("⚠️  Windows sisteminde servis yeniden başlatma desteklenmiyor")
            return True
        else:  # Unix/Linux
            # systemd servis kontrolü
            result = subprocess.run(["systemctl", "is-active", "petvoice"], 
                                  capture_output=True, text=True)
            if result.returncode == 0 and result.stdout.strip() == "active":
                # Servisi yeniden başlat
                subprocess.run(["sudo", "systemctl", "restart", "petvoice"], check=True)
                print("✓ PetVoice servisi yeniden başlatıldı")
            else:
                print("⚠️  PetVoice servisi bulunamadı veya aktif değil")
            
            # Celery servis kontrolü
            result = subprocess.run(["systemctl", "is-active", "petvoice-celery"], 
                                  capture_output=True, text=True)
            if result.returncode == 0 and result.stdout.strip() == "active":
                # Celery servisini yeniden başlat
                subprocess.run(["sudo", "systemctl", "restart", "petvoice-celery"], check=True)
                print("✓ PetVoice Celery servisi yeniden başlatıldı")
            else:
                print("⚠️  PetVoice Celery servisi bulunamadı veya aktif değil")
            
            return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Servisler yeniden başlatılırken hata oluştu: {e}")
        return False
    except Exception as e:
        print(f"✗ Beklenmeyen hata oluştu: {e}")
        return False

def update_version_file(new_version):
    """Sürüm dosyasını günceller"""
    print("Sürüm dosyası güncelleniyor...")
    
    try:
        version_file = Path("VERSION")
        with open(version_file, "w") as f:
            f.write(new_version)
        print(f"✓ Sürüm dosyası güncellendi: {new_version}")
        return True
    except Exception as e:
        print(f"✗ Sürüm dosyası güncellenirken hata oluştu: {e}")
        return False

def show_completion_message():
    """Tamamlanma mesajını gösterir"""
    print("\n" + "="*60)
    print("✅ Uygulama Güncellemesi Tamamlandı!")
    print("="*60)
    print("Yapılan değişiklikler:")
    print("  ✓ En son sürüm alındı")
    print("  ✓ Bağımlılıklar güncellendi")
    print("  ✓ Veritabanı migration'ları çalıştırıldı")
    print("  ✓ Servisler yeniden başlatıldı")
    print()
    print("💡 Kontrol edilmesi gerekenler:")
    print("  - Uygulamanın düzgün çalıştığından emin olun")
    print("  - Yeni özelliklerin doğru çalıştığını test edin")
    print("  - Log dosyalarını kontrol edin")
    print("="*60)

def main():
    """Ana fonksiyon"""
    print("PetVoice AI Güncelleme Betiği")
    print("="*30)
    
    # Mevcut sürümü kontrol et
    current_version = check_current_version()
    
    # Yedekleme yap
    if not backup_current_version():
        print("✗ Yedekleme başarısız oldu. Güncelleme iptal ediliyor.")
        return 1
    
    # Güncelleme adımları
    steps = [
        ("Değişiklikler", pull_latest_changes),
        ("Bağımlılıklar", update_dependencies),
        ("Migration", run_migrations),
        ("Servisler", restart_services)
    ]
    
    failed_steps = []
    
    for step_name, step_function in steps:
        print(f"\n{step_name} güncelleniyor...")
        if not step_function():
            failed_steps.append(step_name)
    
    # Sonuç
    if failed_steps:
        print(f"\n✗ Aşağıdaki adımlarda hata oluştu: {', '.join(failed_steps)}")
        print("Lütfen hataları kontrol edin ve manuel olarak düzeltin.")
        return 1
    else:
        # Sürüm dosyasını güncelle
        new_version = datetime.now().strftime('%Y.%m.%d')
        update_version_file(new_version)
        
        show_completion_message()
        return 0

if __name__ == '__main__':
    sys.exit(main())