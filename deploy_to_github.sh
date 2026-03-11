#!/bin/bash
# deploy_to_github.sh
# GitHub'a otomatik yükleme scripti (Linux/Mac)

set -e  # Hata durumunda dur

# Renkli çıktı için
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}╔════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║     PetVoice AI - GitHub Deployment Script           ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════╝${NC}"
echo ""

# GitHub repository URL
REPO_URL="https://github.com/gkhantyln/petvoice-ai.git"

# 1. Git kontrolü
echo -e "${YELLOW}[1/8] Git kontrolü yapılıyor...${NC}"
if ! command -v git &> /dev/null; then
    echo -e "${RED}✗ Git yüklü değil! Lütfen Git'i yükleyin.${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Git bulundu${NC}"
echo ""

# 2. Hassas dosyaları kontrol et
echo -e "${YELLOW}[2/8] Hassas dosyalar kontrol ediliyor...${NC}"

# .env dosyasını kontrol et
if [ -f ".env" ]; then
    echo -e "${YELLOW}⚠ .env dosyası bulundu${NC}"
    if grep -q "GOOGLE_API_KEY=AIza" .env 2>/dev/null; then
        echo -e "${RED}✗ UYARI: .env dosyasında gerçek API anahtarları var!${NC}"
        echo -e "${YELLOW}  .gitignore'da olduğundan emin olun.${NC}"
    fi
fi

# Veritabanı dosyalarını kontrol et
if ls *.db 1> /dev/null 2>&1; then
    echo -e "${YELLOW}⚠ Veritabanı dosyaları bulundu (.db)${NC}"
    echo -e "${YELLOW}  .gitignore'da olduğundan emin olun.${NC}"
fi

echo -e "${GREEN}✓ Hassas dosya kontrolü tamamlandı${NC}"
echo ""

# 3. .gitignore kontrolü
echo -e "${YELLOW}[3/8] .gitignore kontrolü...${NC}"
if [ ! -f ".gitignore" ]; then
    echo -e "${RED}✗ .gitignore dosyası bulunamadı!${NC}"
    exit 1
fi
echo -e "${GREEN}✓ .gitignore mevcut${NC}"
echo ""

# 4. Git repository başlat (eğer yoksa)
echo -e "${YELLOW}[4/8] Git repository kontrol ediliyor...${NC}"
if [ ! -d ".git" ]; then
    echo -e "${BLUE}  Git repository başlatılıyor...${NC}"
    git init
    echo -e "${GREEN}✓ Git repository başlatıldı${NC}"
else
    echo -e "${GREEN}✓ Git repository zaten mevcut${NC}"
fi
echo ""

# 5. Dosyaları stage'e ekle
echo -e "${YELLOW}[5/8] Dosyalar ekleniyor...${NC}"
git add .
echo -e "${GREEN}✓ Dosyalar eklendi${NC}"
echo ""

# 6. Commit oluştur
echo -e "${YELLOW}[6/8] Commit oluşturuluyor...${NC}"
COMMIT_MSG="feat: Initial commit - PetVoice AI v1.0.0

🎉 İlk sürüm özellikleri:
- Multi-provider AI sistemi (Gemini, OpenAI, Claude)
- Otomatik failover mekanizması
- Ses analizi ve spektrogram görselleştirme
- Kullanıcı yönetimi ve admin paneli
- Responsive web tasarımı
- Türkçe dil desteği"

git commit -m "$COMMIT_MSG"
echo -e "${GREEN}✓ Commit oluşturuldu${NC}"
echo ""

# 7. Remote ekle ve push
echo -e "${YELLOW}[7/8] GitHub'a yükleniyor...${NC}"

# Mevcut remote'u kontrol et
if git remote | grep -q "origin"; then
    echo -e "${BLUE}  Mevcut remote güncelleniyor...${NC}"
    git remote set-url origin "$REPO_URL"
else
    echo -e "${BLUE}  Remote ekleniyor...${NC}"
    git remote add origin "$REPO_URL"
fi

# Branch adını main olarak ayarla
git branch -M main

# Push et
echo -e "${BLUE}  Push yapılıyor...${NC}"
if git push -u origin main; then
    echo -e "${GREEN}✓ GitHub'a başarıyla yüklendi!${NC}"
else
    echo -e "${RED}✗ Push başarısız oldu!${NC}"
    echo -e "${YELLOW}  Muhtemel sebepler:${NC}"
    echo -e "${YELLOW}  - GitHub kimlik doğrulaması gerekiyor${NC}"
    echo -e "${YELLOW}  - Repository'ye yazma izniniz yok${NC}"
    echo -e "${YELLOW}  - İnternet bağlantısı sorunu${NC}"
    exit 1
fi
echo ""

# 8. Tag oluştur
echo -e "${YELLOW}[8/8] Release tag'i oluşturuluyor...${NC}"
git tag -a v1.0.0 -m "Release v1.0.0 - Initial release

🚀 PetVoice AI v1.0.0

Özellikler:
- Multi-provider AI sistemi
- Otomatik failover
- Ses analizi
- Spektrogram görselleştirme
- Admin paneli
- Responsive tasarım"

if git push origin v1.0.0; then
    echo -e "${GREEN}✓ Tag oluşturuldu ve push edildi${NC}"
else
    echo -e "${YELLOW}⚠ Tag push edilemedi (sorun değil)${NC}"
fi
echo ""

# Başarı mesajı
echo -e "${GREEN}╔════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║              🎉 BAŞARILI! 🎉                           ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${BLUE}Repository URL:${NC} $REPO_URL"
echo ""
echo -e "${YELLOW}Sonraki adımlar:${NC}"
echo -e "  1. GitHub'da repository'yi açın"
echo -e "  2. About bölümünü düzenleyin"
echo -e "  3. Topics ekleyin: python, flask, ai, pet-care"
echo -e "  4. README.md'yi kontrol edin"
echo -e "  5. İlk release'i oluşturun (v1.0.0 tag'i zaten var)"
echo ""
echo -e "${GREEN}Tebrikler! Projeniz GitHub'da! 🚀${NC}"
