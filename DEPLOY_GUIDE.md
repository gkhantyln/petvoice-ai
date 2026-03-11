# 🚀 GitHub'a Yükleme Kılavuzu

Bu kılavuz, PetVoice AI projesini GitHub'a otomatik olarak yüklemenizi sağlar.

## 📋 Ön Hazırlık

### 1. Git Kurulumu

**Windows:**
- [Git for Windows](https://git-scm.com/download/win) indirin ve kurun
- Kurulum sırasında varsayılan ayarları kullanın

**Linux:**
```bash
sudo apt-get install git
```

**Mac:**
```bash
brew install git
```

### 2. GitHub Hesabı

- [GitHub](https://github.com) hesabınız olmalı
- Repository'yi oluşturmuş olmalısınız: https://github.com/gkhantyln/petvoice-ai

### 3. Hassas Bilgileri Temizleme

Yüklemeden önce kontrol edin:

```bash
# .env dosyasında gerçek API anahtarları olmamalı
# Veritabanı dosyaları (.db) commit edilmemeli
# uploads/ klasöründeki test dosyaları temizlenmeli
```

## 🎯 Otomatik Yükleme

### Windows (PowerShell)

1. **PowerShell'i Yönetici olarak açın**

2. **Execution Policy'yi ayarlayın** (ilk kez çalıştırıyorsanız):
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

3. **Proje dizinine gidin**:
```powershell
cd C:\Users\user\Desktop\AnimalsVoice
```

4. **Script'i çalıştırın**:
```powershell
.\deploy_to_github.ps1
```

### Linux/Mac (Bash)

1. **Terminal'i açın**

2. **Proje dizinine gidin**:
```bash
cd ~/Desktop/AnimalsVoice
```

3. **Script'e çalıştırma izni verin**:
```bash
chmod +x deploy_to_github.sh
```

4. **Script'i çalıştırın**:
```bash
./deploy_to_github.sh
```

## 🔐 GitHub Kimlik Doğrulama

### İlk Kez Push Yapıyorsanız

Git, GitHub kimlik bilgilerinizi isteyecektir:

**Seçenek 1: Personal Access Token (Önerilen)**

1. [GitHub Settings > Developer settings > Personal access tokens](https://github.com/settings/tokens) adresine gidin
2. "Generate new token (classic)" tıklayın
3. Token adı: `PetVoice AI Deploy`
4. Scope: `repo` seçin
5. Token'ı oluşturun ve kopyalayın
6. Git şifre istediğinde token'ı yapıştırın

**Seçenek 2: SSH Key**

```bash
# SSH key oluştur
ssh-keygen -t ed25519 -C "your_email@example.com"

# Public key'i kopyala
cat ~/.ssh/id_ed25519.pub

# GitHub'da Settings > SSH and GPG keys > New SSH key
# Kopyaladığınız key'i yapıştırın
```

## 📝 Script Ne Yapar?

Script otomatik olarak şu adımları gerçekleştirir:

1. ✅ **Git Kontrolü** - Git yüklü mü kontrol eder
2. ✅ **Hassas Dosya Kontrolü** - .env ve .db dosyalarını kontrol eder
3. ✅ **Git Repository** - Gerekirse git repository başlatır
4. ✅ **Dosyaları Ekle** - Tüm dosyaları stage'e ekler
5. ✅ **Commit Oluştur** - Anlamlı commit mesajı ile commit oluşturur
6. ✅ **Remote Ekle** - GitHub repository'yi remote olarak ekler
7. ✅ **Push** - Dosyaları GitHub'a yükler
8. ✅ **Tag Oluştur** - v1.0.0 release tag'i oluşturur

## ⚠️ Yaygın Sorunlar ve Çözümleri

### Sorun 1: "git: command not found"

**Çözüm:** Git yüklü değil. Yukarıdaki Git kurulum adımlarını takip edin.

### Sorun 2: "Permission denied (publickey)"

**Çözüm:** SSH key yapılandırması gerekli veya HTTPS kullanın.

```bash
# HTTPS kullanmak için
git remote set-url origin https://github.com/gkhantyln/petvoice-ai.git
```

### Sorun 3: "Authentication failed"

**Çözüm:** Personal Access Token kullanın:
- Kullanıcı adı: GitHub kullanıcı adınız
- Şifre: Personal Access Token

### Sorun 4: "Updates were rejected"

**Çözüm:** Repository'de değişiklikler var. Önce pull yapın:

```bash
git pull origin main --rebase
git push origin main
```

### Sorun 5: ".env dosyasında API anahtarları var"

**Çözüm:** 
1. .env dosyasını .gitignore'a ekleyin (zaten eklenmeli)
2. Eğer yanlışlıkla commit ettiyseniz:

```bash
# Son commit'i geri al
git reset --soft HEAD~1

# .env'yi kaldır
git rm --cached .env

# Tekrar commit et
git commit -m "fix: Remove .env from git"
```

## 🎨 GitHub Repository Ayarları

Yükleme tamamlandıktan sonra:

### 1. About Bölümü

Repository sayfasında sağ üstteki ⚙️ (Settings) ikonuna tıklayın:

- **Description:** `🐾 AI-powered pet sound analysis platform using Google Gemini AI`
- **Website:** Demo URL'niz (varsa)
- **Topics:** `python`, `flask`, `ai`, `machine-learning`, `pet-care`, `sound-analysis`, `google-gemini`, `web-application`

### 2. README.md Kontrolü

- GitHub'da README.md'nin düzgün görüntülendiğini kontrol edin
- Görseller ve linkler çalışıyor mu?
- Badge'ler doğru mu?

### 3. İlk Release Oluşturma

1. Repository'de "Releases" sekmesine gidin
2. "Draft a new release" tıklayın
3. Tag: `v1.0.0` (script tarafından oluşturuldu)
4. Title: `PetVoice AI v1.0.0 - Initial Release`
5. Description: CHANGELOG.md'den kopyalayın
6. "Publish release" tıklayın

### 4. Issues ve Discussions

- **Issues:** Aktif (hata bildirimleri için)
- **Discussions:** Aktif (topluluk için)
- **Projects:** İsteğe bağlı
- **Wiki:** İsteğe bağlı

## 📊 Sonraki Güncellemeler

Gelecekte değişiklik yaptığınızda:

```bash
# Değişiklikleri ekle
git add .

# Commit oluştur
git commit -m "feat: Yeni özellik açıklaması"

# Push et
git push origin main
```

### Commit Mesajı Formatı

```
<tip>: <kısa açıklama>

[detaylı açıklama]
```

**Tipler:**
- `feat`: Yeni özellik
- `fix`: Hata düzeltme
- `docs`: Dokümantasyon
- `style`: Kod formatı
- `refactor`: Kod iyileştirme
- `test`: Test ekleme
- `chore`: Genel bakım

## 🔄 Yeni Sürüm Yayınlama

```bash
# Yeni tag oluştur
git tag -a v1.1.0 -m "Release v1.1.0 - Yeni özellikler"

# Tag'i push et
git push origin v1.1.0

# GitHub'da release oluştur
```

## 📞 Yardım

Sorun yaşıyorsanız:

1. Script çıktısını kontrol edin
2. Git durumunu kontrol edin: `git status`
3. Remote'u kontrol edin: `git remote -v`
4. [GitHub Issues](https://github.com/gkhantyln/petvoice-ai/issues) açın

## ✅ Kontrol Listesi

Yüklemeden önce:

- [ ] Git yüklü
- [ ] GitHub hesabı var
- [ ] Repository oluşturuldu
- [ ] .env dosyası .gitignore'da
- [ ] Gerçek API anahtarları kodda yok
- [ ] Veritabanı dosyaları .gitignore'da
- [ ] Test dosyaları temizlendi

Yüklemeden sonra:

- [ ] Repository'de dosyalar görünüyor
- [ ] README.md düzgün görünüyor
- [ ] About bölümü dolduruldu
- [ ] Topics eklendi
- [ ] v1.0.0 tag'i var
- [ ] İlk release oluşturuldu

---

**Başarılar! 🚀**
