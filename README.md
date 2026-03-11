# 🐾 PetVoice AI - Hayvan Sesi Analiz Platformu

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![AI](https://img.shields.io/badge/AI-Google%20Gemini-red.svg)

**Yapay zeka destekli profesyonel hayvan sesi analiz platformu**

[Özellikler](#-özellikler) • [Kurulum](#-kurulum) • [Kullanım](#-kullanım) • [Dokümantasyon](#-dokümantasyon) • [Katkıda Bulunma](#-katkıda-bulunma)

### 🎥 Demo Video

[![PetVoice AI Demo](https://img.youtube.com/vi/FpICvQ-c_i8/0.jpg)](https://youtu.be/FpICvQ-c_i8)

**[▶️ Videoyu İzle](https://youtu.be/FpICvQ-c_i8)**

</div>

---

## 📖 Hakkında

PetVoice AI, evcil hayvanların seslerini analiz ederek duygusal durumlarını, ihtiyaçlarını ve sağlık durumlarını anlamaya yardımcı olan gelişmiş bir web platformudur. Google Gemini AI teknolojisi ile desteklenen platform, ses analizi, spektrogram görselleştirme ve kullanıcı dostu arayüzü ile hayvan sahiplerine profesyonel düzeyde içgörüler sunar.

## ✨ Özellikler

### 🎯 Temel Özellikler
- **Multi-Provider AI Sistemi**: Google Gemini, OpenAI, Anthropic Claude desteği
- **Otomatik Failover**: Bir API çalışmazsa otomatik olarak diğerine geçiş
- **Çoklu API Anahtarı**: Her provider için birden fazla anahtar desteği
- **AI Destekli Analiz**: Gelişmiş ses analizi
- **Spektrogram Görselleştirme**: İnteraktif ve detaylı ses görselleştirme
- **Tarayıcı Kaydı**: Doğrudan tarayıcıdan ses kaydı yapabilme
- **Çoklu Format Desteği**: WAV, MP3, OGG, FLAC formatlarını destekler
- **Evcil Hayvan Yönetimi**: Birden fazla evcil hayvan profili oluşturma
- **Analiz Geçmişi**: Tüm analizlerin detaylı geçmişi

### 🔐 Güvenlik ve Yönetim
- **Kullanıcı Kimlik Doğrulama**: Güvenli kayıt ve giriş sistemi
- **Admin Paneli**: Kapsamlı yönetim arayüzü
- **Profil Yönetimi**: Kullanıcı profili ve ayarları
- **Rate Limiting**: API isteklerini sınırlama

### 🎨 Kullanıcı Deneyimi
- **Responsive Tasarım**: Tüm cihazlarda mükemmel görünüm
- **Kullanıcı Dostu Arayüz**: Sezgisel ve kolay kullanım
- **Hata Yönetimi**: Anlaşılır hata mesajları
- **Türkçe Dil Desteği**: Tam Türkçe arayüz

## 🛠️ Teknoloji Stack

### Backend
- **Flask 3.0+** - Modern Python web framework
- **SQLAlchemy** - ORM ve veritabanı yönetimi
- **Google Gemini AI** - Ses analizi için yapay zeka
- **Librosa** - Ses işleme ve analiz
- **Matplotlib** - Spektrogram görselleştirme

### Frontend
- **Bootstrap 5** - Responsive CSS framework
- **Vanilla JavaScript** - Client-side işlemler
- **Web Audio API** - Tarayıcı ses kaydı

### Veritabanı
- **SQLite** - Geliştirme ortamı (varsayılan)
- **PostgreSQL** - Production ortamı (önerilen)

## 📁 Proje Yapısı

```
PetVoice-AI/
├── app/                      # Ana uygulama paketi
│   ├── models/              # Veritabanı modelleri
│   ├── views/               # Route ve view fonksiyonları
│   ├── templates/           # HTML şablonları
│   ├── static/              # CSS, JS, resimler
│   └── utils/               # Yardımcı fonksiyonlar
├── scripts/                 # Yardımcı scriptler
│   ├── setup/              # Kurulum scriptleri
│   ├── tests/              # Test dosyaları
│   └── debug/              # Debug araçları
├── deploy/                  # Deployment dosyaları
├── docs/                    # Dokümantasyon
├── migrations/              # Veritabanı migration'ları
├── uploads/                 # Yüklenen dosyalar
├── config.py               # Yapılandırma ayarları
├── run.py                  # Uygulama başlatıcı
└── requirements.txt        # Python bağımlılıkları
```

## 🚀 Kurulum

### Gereksinimler

- Python 3.8 veya üzeri
- pip (Python paket yöneticisi)
- FFmpeg (ses formatı dönüşümleri için)
- Google Gemini API anahtarı

### Adım Adım Kurulum

1. **Projeyi klonlayın**
```bash
git clone https://github.com/kullaniciadi/petvoice-ai.git
cd petvoice-ai
```

2. **Sanal ortam oluşturun ve aktifleştirin**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

3. **Bağımlılıkları yükleyin**
```bash
pip install -r requirements.txt
```

4. **FFmpeg'i yükleyin**

**Windows:**
- [FFmpeg'i indirin](https://ffmpeg.org/download.html)
- `C:\ffmpeg\bin` klasörüne çıkarın
- Sistem PATH'ine ekleyin

**Linux:**
```bash
sudo apt-get install ffmpeg
```

**Mac:**
```bash
brew install ffmpeg
```

5. **Ortam değişkenlerini ayarlayın**

`.env` dosyasını oluşturun ve düzenleyin:
```bash
cp .env.example .env
```

`.env` dosyasında şu değerleri güncelleyin:
```env
# Google Gemini API Anahtarı (Zorunlu)
# https://aistudio.google.com/app/apikey
GOOGLE_API_KEY=your_api_key_here

# Opsiyonel: Yedek API anahtarları (Failover için)
GOOGLE_API_KEY_1=your_backup_key_1
GOOGLE_API_KEY_2=your_backup_key_2

# Opsiyonel: Alternatif AI Provider'lar
OPENAI_API_KEY=your_openai_key_here
ANTHROPIC_API_KEY=your_claude_key_here

# Flask gizli anahtarı
SECRET_KEY=your_secret_key_here

# Veritabanı (SQLite varsayılan)
DATABASE_URL=sqlite:///petvoice.db
```

**Multi-Provider Desteği:**
- Birden fazla AI provider kullanabilirsiniz
- Bir API çalışmazsa otomatik olarak diğerine geçer
- Detaylar için: [Multi-Provider Kılavuzu](docs/MULTI_PROVIDER_GUIDE.md)

6. **Veritabanını başlatın**
```bash
python scripts/setup/init_db.py
```

7. **Uygulamayı çalıştırın**
```bash
python run.py
```

Uygulama `http://localhost:5000` adresinde çalışacaktır.

### 🔑 Varsayılan Admin Hesabı

İlk giriş için:
- **Kullanıcı adı:** `admin`
- **Şifre:** `admin123`

⚠️ **Önemli:** İlk girişten sonra şifrenizi değiştirin!

## 💻 Kullanım

### Evcil Hayvan Ekleme

1. Giriş yapın
2. "Evcil Hayvanlarım" menüsüne gidin
3. "Yeni Evcil Hayvan Ekle" butonuna tıklayın
4. Gerekli bilgileri doldurun

### Ses Analizi Yapma

1. "Ses Analizi" menüsüne gidin
2. Evcil hayvanınızı seçin
3. Ses dosyası yükleyin veya tarayıcıdan kaydedin
4. Durumu belirtin (opsiyonel)
5. "Analiz Et" butonuna tıklayın

### Sonuçları Görüntüleme

- Analiz tamamlandığında otomatik olarak sonuç sayfasına yönlendirilirsiniz
- Spektrogram görselini inceleyebilirsiniz
- AI analizini okuyabilirsiniz
- Geçmiş analizlerinizi "Analiz Geçmişi" menüsünden görüntüleyebilirsiniz

## 🔧 Yapılandırma

### Veritabanı Yapılandırması

**SQLite (Varsayılan - Geliştirme):**
```python
DATABASE_URL=sqlite:///petvoice.db
```

**PostgreSQL (Production):**
```python
DATABASE_URL=postgresql://kullanici:sifre@localhost/petvoice
```

### Dosya Yükleme Ayarları

`config.py` dosyasında:
```python
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
UPLOAD_FOLDER = 'uploads'
```

## 🧪 Test

Testleri çalıştırmak için:
```bash
python scripts/run_tests.py
```

## 📊 API Kullanımı

### Ses Analizi API

```python
POST /analysis/upload
Content-Type: multipart/form-data

Parameters:
- sound_file: Ses dosyası
- pet_id: Evcil hayvan ID
- context_situation: Durum (opsiyonel)
- custom_context: Özel açıklama (opsiyonel)
```

## 🐳 Docker ile Çalıştırma

```bash
# Docker container'ı oluştur ve çalıştır
docker-compose up -d

# Logları görüntüle
docker-compose logs -f

# Durdur
docker-compose down
```

## 🔒 Güvenlik

- CSRF koruması aktif
- Rate limiting uygulanmış
- Güvenli şifre hashleme (bcrypt)
- Input validasyonu
- XSS koruması

## 🤝 Katkıda Bulunma

Katkılarınızı bekliyoruz! Lütfen şu adımları izleyin:

1. Fork edin
2. Feature branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Değişikliklerinizi commit edin (`git commit -m 'feat: Add amazing feature'`)
4. Branch'inizi push edin (`git push origin feature/amazing-feature`)
5. Pull Request açın

### Commit Mesajı Formatı

```
feat: Yeni özellik ekleme
fix: Hata düzeltme
docs: Dokümantasyon değişikliği
style: Kod formatı değişikliği
refactor: Kod yeniden yapılandırma
test: Test ekleme/düzeltme
chore: Genel bakım işleri
```

## 📝 Lisans

Bu proje MIT lisansı altında lisanslanmıştır. Detaylar için [LICENSE](LICENSE) dosyasına bakın.

## 🙏 Teşekkürler

- [Google Gemini AI](https://ai.google.dev/) - AI analiz yetenekleri
- [Flask](https://flask.palletsprojects.com/) - Web framework
- [Librosa](https://librosa.org/) - Ses işleme kütüphanesi
- [Bootstrap](https://getbootstrap.com/) - UI framework

## 📞 İletişim

Sorularınız veya önerileriniz için:

- **GitHub Issues**: [Sorun bildirin](https://github.com/gkhamtyln/petvoice-ai/issues)
- **Email**: tylngkhn@gmail.com

## 🗺️ Yol Haritası

- [ ] Mobil uygulama geliştirme
- [ ] Çoklu dil desteği
- [ ] Gerçek zamanlı ses analizi
- [ ] Veteriner danışmanlık entegrasyonu
- [ ] Sosyal özellikler (topluluk)
- [ ] API dokümantasyonu (Swagger)

---

<div align="center">

**[⬆ Başa Dön](#-petvoice-ai---hayvan-sesi-analiz-platformu)**

Made with ❤️ for pet lovers

</div>
