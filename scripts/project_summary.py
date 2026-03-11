#!/usr/bin/env python3
# project_summary.py
# Proje özeti oluşturucu
# Bu dosya, projenin teknik özetini oluşturur

import os
import sys
from pathlib import Path
from datetime import datetime

def count_files_and_lines():
    """Dosya ve satır sayılarını sayar"""
    file_counts = {}
    total_lines = 0
    total_files = 0
    
    # Sayılacak dosya uzantıları
    extensions = {
        '.py': 'Python',
        '.html': 'HTML',
        '.css': 'CSS',
        '.js': 'JavaScript',
        '.md': 'Markdown',
        '.txt': 'Text',
        '.json': 'JSON',
        '.yaml': 'YAML',
        '.yml': 'YAML'
    }
    
    # Başlangıç dizini
    start_path = '.'
    
    for root, dirs, files in os.walk(start_path):
        # Git ve diğer sistem dizinlerini atla
        dirs[:] = [d for d in dirs if d not in ['.git', '__pycache__', 'venv', '.vscode', '.idea']]
        
        for file in files:
            file_path = os.path.join(root, file)
            
            # Dosya uzantısını al
            _, ext = os.path.splitext(file)
            
            if ext in extensions:
                # Dosya sayısını artır
                file_counts[extensions[ext]] = file_counts.get(extensions[ext], 0) + 1
                total_files += 1
                
                # Satır sayısını hesapla
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        lines = sum(1 for _ in f)
                        total_lines += lines
                except Exception:
                    pass  # Dosya okunamazsa atla
    
    return file_counts, total_files, total_lines

def get_project_structure():
    """Proje yapısını alır"""
    structure = []
    
    def walk_directory(path, prefix="", is_last=True):
        path_obj = Path(path)
        if path_obj.name in ['.git', '__pycache__', 'venv', '.vscode', '.idea']:
            return
        
        # Dizin adını ekle
        if prefix:
            structure.append(f"{prefix}{'└── ' if is_last else '├── '}{path_obj.name}/")
        else:
            structure.append(f"{path_obj.name}/")
        
        # Alt dizin ve dosyaları al
        try:
            items = list(path_obj.iterdir())
            dirs = [item for item in items if item.is_dir()]
            files = [item for item in items if item.is_file()]
            
            # Önce dizinleri, sonra dosyaları işle
            all_items = dirs + files
            
            for i, item in enumerate(all_items):
                is_last_item = (i == len(all_items) - 1)
                current_prefix = prefix + ("    " if is_last else "│   ")
                
                if item.is_dir():
                    walk_directory(item, current_prefix, is_last_item)
                else:
                    # Sadece önemli dosyaları göster
                    if item.name in ['README.md', 'requirements.txt', 'run.py', 'config.py'] or \
                       item.suffix in ['.py', '.html', '.css', '.js']:
                        structure.append(f"{current_prefix}{'└── ' if is_last_item else '├── '}{item.name}")
        except Exception:
            pass
    
    walk_directory('.')
    return structure

def get_technology_stack():
    """Teknoloji yığınını alır"""
    technologies = {
        "Backend Framework": "Flask (Python)",
        "Veritabanı": "PostgreSQL / SQLite",
        "AI": "Google Gemini",
        "Frontend": "HTML5, CSS3, JavaScript, Bootstrap 5",
        "Arka Plan İşleri": "Celery + Redis",
        "Test Framework": "unittest",
        "Deployment": "Gunicorn + Nginx"
    }
    
    return technologies

def get_features():
    """Özellikleri listeler"""
    features = [
        "Ses kaydı ve yükleme",
        "AI destekli ses analizi",
        "Kullanıcı ve evcil hayvan profili yönetimi",
        "Analiz geçmişi ve istatistikler",
        "Responsive web arayüzü",
        "Yönetici paneli",
        "Arka plan görev işleme",
        "REST API",
        "Kimlik doğrulama ve yetkilendirme",
        "Dosya yönetimi"
    ]
    
    return features

def generate_summary():
    """Proje özetini oluşturur"""
    # Dosya ve satır sayılarını al
    file_counts, total_files, total_lines = count_files_and_lines()
    
    # Proje yapısını al
    structure = get_project_structure()
    
    # Teknoloji yığınını al
    technologies = get_technology_stack()
    
    # Özellikleri al
    features = get_features()
    
    # Özet raporu oluştur
    summary = f"""# 🐾 PetVoice AI Proje Özeti

## 📊 Proje İstatistikleri

- **Toplam Dosya Sayısı**: {total_files}
- **Toplam Satır Sayısı**: {total_lines:,}

### Dosya Türleri:
"""
    
    for lang, count in sorted(file_counts.items()):
        summary += f"- {lang}: {count} dosya\n"
    
    summary += f"""

## 🏗️ Teknoloji Yığını

"""
    
    for tech, desc in technologies.items():
        summary += f"- **{tech}**: {desc}\n"
    
    summary += f"""

## ✨ Özellikler

"""
    
    for i, feature in enumerate(features, 1):
        summary += f"{i}. {feature}\n"
    
    summary += f"""

## 📁 Proje Yapısı

```
"""
    
    # Yapıdan sadece ilk 50 satırı al
    for line in structure[:50]:
        summary += line + "\n"
    
    if len(structure) > 50:
        summary += f"... ve {len(structure) - 50} daha fazla\n"
    
    summary += f"""```

## 📅 Rapor Bilgileri

- **Oluşturulma Tarihi**: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}
- **Python Sürümü**: {sys.version.split()[0]}
- **İşletim Sistemi**: {os.name}

---
*Bu rapor otomatik olarak oluşturulmuştur.*
"""
    
    return summary

def main():
    """Ana fonksiyon"""
    print("PetVoice AI Proje Özeti Oluşturuluyor...")
    
    # Özet oluştur
    summary = generate_summary()
    
    # Dosyaya yaz
    summary_file = "PROJECT_SUMMARY.md"
    with open(summary_file, "w", encoding="utf-8") as f:
        f.write(summary)
    
    print(f"✓ Proje özeti oluşturuldu: {summary_file}")
    
    # Ekrana da yazdır
    print("\n" + "="*60)
    print("ÖZET")
    print("="*60)
    
    # Basit istatistikler
    file_counts, total_files, total_lines = count_files_and_lines()
    print(f"Toplam Dosya: {total_files}")
    print(f"Toplam Satır: {total_lines:,}")
    
    print("\nTeknoloji Yığını:")
    technologies = get_technology_stack()
    for tech, desc in list(technologies.items())[:5]:  # İlk 5 teknoloji
        print(f"  - {tech}: {desc}")
    
    if len(technologies) > 5:
        print(f"  ... ve {len(technologies) - 5} daha fazla")
    
    print(f"\nDetaylı rapor: {summary_file}")

if __name__ == '__main__':
    main()