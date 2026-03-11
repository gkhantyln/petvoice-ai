# 🚀 Hızlı Başlangıç Rehberi

PetVoice AI'yi 5 dakikada çalıştırın!

## ⚡ Hızlı Kurulum

### 1. Projeyi İndirin
```bash
git clone https://github.com/kullaniciadi/petvoice-ai.git
cd petvoice-ai
```

### 2. Sanal Ortam Oluşturun
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Bağımlılıkları Yükleyin
```bash
pip install -r requirements.txt
```

### 4. API Anahtarı Alın
1. [Google AI Studio](https://aistudio.google.com/app/apikey) adresine gidin
2. "Create API Key" butonuna tıklayın
3. Anahtarı kopyalayın

### 5. Ortam Değişkenlerini Ayarlayın
```bash
# .env dosyası oluşturun
cp .env.example .env
```

`.env` dosyasını düzenleyin:
```env
GOOGLE_API_KEY=buraya_api_anahtarinizi_yapiştirin
SECRET_KEY=güvenli_bir_anahtar_oluşturun
```

### 6. Veritabanını Başlatın
```bash
python scripts/setup/init_db.py
```

### 7. Uygulamayı Çalıştırın
```bash
python run.py
```

🎉 **Tebrikler!** Uygulama http://localhost:5000 adresinde çalışıyor.

## 🔐 İlk Giriş

**Varsayılan Admin Hesabı:**
- Kullanıcı adı: `admin`
- Şifre: `admin123`

⚠️ İlk girişten sonra şifrenizi değiştirin!

## 📱 İlk Analiz

1. **Giriş Yapın**
   - http://localhost:5000/auth/login adresine gidin
   - Admin bilgileriyle giriş yapın

2. **Evcil Hayvan Ekleyin**
   - "Evcil Hayvanlarım" menüsüne tıklayın
   - "Yeni Evcil Hayvan Ekle" butonuna tıklayın
   - Bilgileri doldurun ve kaydedin

3. **Ses Analizi Yapın**
   - "Ses Analizi" menüsüne gidin
   - Evcil hayvanınızı seçin
   - Ses dosyası yükleyin veya kaydedin
   - "Analiz Et" butonuna tıklayın

4. **Sonuçları Görüntüleyin**
   - AI analizi otomatik olarak gösterilir
   - Spektrogramı inceleyebilirsiniz
   - Geçmiş analizlerinizi görüntüleyebilirsiniz

## 🎯 Sonraki Adımlar

- [Detaylı Dokümantasyon](README.md)
- [Katkıda Bulunma](CONTRIBUTING.md)
- [Değişiklik Günlüğü](CHANGELOG.md)

## ❓ Sorun mu Yaşıyorsunuz?

### FFmpeg Hatası
```bash
# Windows
# FFmpeg'i indirin ve C:\ffmpeg\bin klasörüne çıkarın

# Linux
sudo apt-get install ffmpeg

# Mac
brew install ffmpeg
```

### API Anahtarı Hatası
- API anahtarınızın geçerli olduğundan emin olun
- .env dosyasında doğru ayarlandığını kontrol edin
- Uygulamayı yeniden başlatın

### Port Zaten Kullanımda
```bash
# Farklı bir port kullanın
python run.py --port 5001
```

### Veritabanı Hatası
```bash
# Veritabanını sıfırlayın
rm petvoice.db
python scripts/setup/init_db.py
```

## 💡 İpuçları

- **En İyi Sonuçlar İçin:** WAV formatında ses dosyaları kullanın
- **Hızlı Test:** Tarayıcıdan doğrudan ses kaydı yapabilirsiniz
- **Analiz Geçmişi:** Tüm analizleriniz kaydedilir ve tekrar görüntülenebilir
- **Spektrogram:** Sesin frekans dağılımını görsel olarak inceleyin

## 🆘 Yardım

Sorun yaşıyorsanız:
- [GitHub Issues](https://github.com/kullaniciadi/petvoice-ai/issues)
- [Dokümantasyon](README.md)
- Email: your-email@example.com

---

**Keyifli Kullanımlar! 🐾**
