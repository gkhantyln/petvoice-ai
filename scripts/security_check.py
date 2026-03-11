#!/usr/bin/env python3
# security_check.py
# Güvenlik kontrolü betiği
# Bu dosya, uygulamadaki güvenlik açıklarını kontrol eder

import os
import sys
import subprocess
import re
from pathlib import Path

def check_python_security():
    """Python güvenlik açıklarını kontrol eder"""
    print("Python güvenlik açıkları kontrol ediliyor...")
    
    try:
        # pip-audit kontrolü
        result = subprocess.run([sys.executable, "-m", "pip", "audit"], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✓ Python paketlerinde bilinen güvenlik açığı bulunamadı")
            return True
        else:
            print("⚠️  Python paketlerinde güvenlik açığı bulunabilir:")
            print(result.stdout)
            return False
    except FileNotFoundError:
        print("⚠️  pip-audit bulunamadı. Kurulum için: pip install pip-audit")
        return True
    except Exception as e:
        print(f"✗ Python güvenlik kontrolü sırasında hata oluştu: {e}")
        return False

def check_hardcoded_secrets():
    """Kod içinde hardcoded şifreleri kontrol eder"""
    print("Hardcoded şifreler kontrol ediliyor...")
    
    # Aranacak desenler
    secret_patterns = [
        r'password\s*=\s*["\'][^"\']+["\']',
        r'secret\s*=\s*["\'][^"\']+["\']',
        r'key\s*=\s*["\'][^"\']+["\']',
        r'token\s*=\s*["\'][^"\']+["\']',
        r'api[_-]?key\s*=\s*["\'][^"\']+["\']'
    ]
    
    # Dosya uzantıları
    file_extensions = ['.py', '.js', '.env', '.json', '.yaml', '.yml']
    
    found_secrets = []
    
    # Tüm dosyalarda ara
    for root, dirs, files in os.walk('.'):
        # Git dizinlerini atla
        if '.git' in dirs:
            dirs.remove('.git')
        
        for file in files:
            if any(file.endswith(ext) for ext in file_extensions):
                file_path = os.path.join(root, file)
                
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        
                        for pattern in secret_patterns:
                            matches = re.findall(pattern, content, re.IGNORECASE)
                            for match in matches:
                                # Basit filtreleme
                                if not any(ignore in match.lower() for ignore in 
                                         ['password"', "''", '""', 'placeholder']):
                                    found_secrets.append((file_path, match))
                except Exception:
                    continue  # Dosya okunamazsa atla
    
    if found_secrets:
        print("⚠️  Potansiyel hardcoded şifreler bulundu:")
        for file_path, secret in found_secrets:
            print(f"  - {file_path}: {secret}")
        return False
    else:
        print("✓ Hardcoded şifre bulunamadı")
        return True

def check_file_permissions():
    """Dosya izinlerini kontrol eder"""
    print("Dosya izinleri kontrol ediliyor...")
    
    # Hassas dosyalar
    sensitive_files = [
        '.env',
        'config.py',
        'app/config.py'
    ]
    
    issues_found = False
    
    for file_path in sensitive_files:
        path = Path(file_path)
        if path.exists():
            # Dosya izinlerini kontrol et
            try:
                stat = path.stat()
                mode = stat.st_mode
                
                # Sadece sahibin okuyup yazabildiği kontrolü (600)
                if mode & 0o777 != 0o600:
                    print(f"⚠️  {file_path} dosyasının izinleri çok açık: {oct(mode & 0o777)}")
                    issues_found = True
            except Exception as e:
                print(f"✗ {file_path} izinleri kontrol edilirken hata oluştu: {e}")
                issues_found = True
    
    if not issues_found:
        print("✓ Dosya izinleri uygun")
    
    return not issues_found

def check_dependencies():
    """Bağımlılık güvenlik açıklarını kontrol eder"""
    print("Bağımlılık güvenlik açıkları kontrol ediliyor...")
    
    try:
        # safety kontrolü
        result = subprocess.run([sys.executable, "-m", "safety", "check"], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✓ Bağımlılıklarda bilinen güvenlik açığı bulunamadı")
            return True
        else:
            print("⚠️  Bağımlılıklarda güvenlik açığı bulunabilir:")
            print(result.stdout)
            return False
    except FileNotFoundError:
        print("⚠️  safety bulunamadı. Kurulum için: pip install safety")
        return True
    except Exception as e:
        print(f"✗ Bağımlılık güvenlik kontrolü sırasında hata oluştu: {e}")
        return False

def check_sql_injection():
    """Basit SQL injection kontrolü"""
    print("SQL injection riskleri kontrol ediliyor...")
    
    # Riskli desenler
    sql_patterns = [
        r'\.execute\s*\([^)]*[%s\?]*[^)]*\)\s*%',
        r'\.execute\s*\([^)]*\+\s*\w+',
        r'\.query\s*\([^)]*\+\s*\w+'
    ]
    
    issues_found = False
    
    # Python dosyalarında ara
    for root, dirs, files in os.walk('app'):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        
                        for pattern in sql_patterns:
                            matches = re.findall(pattern, content)
                            if matches:
                                print(f"⚠️  Potansiyel SQL injection riski: {file_path}")
                                issues_found = True
                                break
                except Exception:
                    continue
    
    if not issues_found:
        print("✓ SQL injection riski bulunamadı")
    
    return not issues_found

def check_xss_vulnerabilities():
    """Basit XSS güvenlik açıklarını kontrol eder"""
    print("XSS güvenlik açıkları kontrol ediliyor...")
    
    # Riskli desenler
    xss_patterns = [
        r'render_template_string\s*\([^)]*\w+',
        r'Markup\s*\([^)]*\w+',
        r'\|\s*safe',
        r'render_template\s*\([^,]*,\s*\w+\s*='
    ]
    
    issues_found = False
    
    # Template dosyalarında ara
    template_dirs = ['app/templates', 'templates']
    
    for template_dir in template_dirs:
        if os.path.exists(template_dir):
            for root, dirs, files in os.walk(template_dir):
                for file in files:
                    if file.endswith(('.html', '.htm', '.xml')):
                        file_path = os.path.join(root, file)
                        
                        try:
                            with open(file_path, 'r', encoding='utf-8') as f:
                                content = f.read()
                                
                                # Jinja2 template'lerinde raw output kontrolü
                                if '{{' in content and '|' not in content and 'safe' not in content:
                                    # Basit kontrol, daha kapsamlı analiz gerekli
                                    pass
                                
                                for pattern in xss_patterns:
                                    matches = re.findall(pattern, content, re.IGNORECASE)
                                    if matches:
                                        print(f"⚠️  Potansiyel XSS riski: {file_path}")
                                        issues_found = True
                                        break
                        except Exception:
                            continue
    
    if not issues_found:
        print("✓ XSS güvenlik açığı bulunamadı")
    
    return not issues_found

def show_security_report(results):
    """Güvenlik raporu gösterir"""
    print("\n" + "="*60)
    print("🔒 Güvenlik Kontrol Raporu")
    print("="*60)
    
    passed = sum(1 for result in results if result)
    total = len(results)
    
    print(f"Sonuç: {passed}/{total} kontrol başarılı")
    
    if passed == total:
        print("✅ Uygulama güvenlik açısından iyi durumda görünüyor")
        print("\n💡 Öneriler:")
        print("  - Düzenli olarak güvenlik kontrolleri yapın")
        print("  - Bağımlılıkları güncel tutun")
        print("  - Kod incelemeleri yapın")
        print("  - Penetration testleri yaptırın")
    else:
        print("⚠️  Uygulamada bazı güvenlik riskleri bulunuyor")
        print("Lütfen yukarıdaki uyarıları dikkate alın ve gerekli düzeltmeleri yapın")
    
    print("="*60)

def main():
    """Ana fonksiyon"""
    print("PetVoice AI Güvenlik Kontrolü")
    print("="*30)
    
    # Güvenlik kontrol adımları
    checks = [
        ("Python Güvenlik", check_python_security),
        ("Hardcoded Şifreler", check_hardcoded_secrets),
        ("Dosya İzinleri", check_file_permissions),
        ("Bağımlılık Güvenliği", check_dependencies),
        ("SQL Injection", check_sql_injection),
        ("XSS Açıkları", check_xss_vulnerabilities)
    ]
    
    results = []
    
    for check_name, check_function in checks:
        print(f"\n{check_name} Kontrolü:")
        result = check_function()
        results.append(result)
        print()
    
    # Raporu göster
    show_security_report(results)
    
    # Çıkış kodunu belirle
    return 0 if all(results) else 1

if __name__ == '__main__':
    sys.exit(main())