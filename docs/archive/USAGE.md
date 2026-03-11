# 🐾 PetVoice AI Kullanım Kılavuzu

Bu belge, PetVoice AI uygulamasının nasıl kurulacağını ve kullanılacağını açıklar.

## 🚀 Kurulum

### Gereksinimler

- Python 3.8 veya üzeri
- PostgreSQL veritabanı (geliştirme için SQLite da kullanılabilir)
- Redis sunucusu
- Google Gemini API anahtarı

### 1. Bağımlılıkların Kurulumu

```bash
pip install -r requirements.txt
```

### 2. Ortam Değişkenlerinin Ayarlanması

Aşağıdaki ortam değişkenlerini ayarlayın:

```bash
export SECRET_KEY="gizli-anahtar"
export DATABASE_URL="postgresql://kullanici:sifre@localhost/petvoice"
export GOOGLE_API_KEY="google-gemini-api-anahtarınız"
export CELERY_BROKER_URL="redis://localhost:6379/0"
export CELERY_RESULT_BACKEND="redis://localhost:6379/0"
```

### 3. Veritabanının Başlatılması

```bash
python init_db.py
```

### 4. Uygulamanın Çalıştırılması

#### Geliştirme Ortamı

```bash
python start_dev.py
```

#### Üretim Ortamı

```bash
# Redis sunucusunu başlatın
redis-server

# Celery worker'ı başlatın
celery -A app.celery_worker.celery worker --loglevel=info

# Flask uygulamasını başlatın
python run.py
```

## 📋 Kullanım

### 1. Kayıt ve Giriş

1. Uygulamayı başlattıktan sonra tarayıcınızda `http://localhost:5000` adresine gidin
2. "Kayıt Ol" butonuna tıklayın
3. Gerekli bilgileri girerek kayıt olun
4. Giriş yapın

### 2. Evcil Hayvan Ekleme

1. Giriş yaptıktan sonra "Evcil Hayvanlarım" sayfasına gidin
2. "Yeni Evcil Hayvan Ekle" butonuna tıklayın
3. Evcil hayvanınızın bilgilerini girin:
   - Ad
   - Tür (kedi, köpek, vs.)
   - Cins (isteğe bağlı)
   - Yaş (isteğe bağlı)
   - Cinsiyet (isteğe bağlı)
   - Ağırlık (isteğe bağlı)
   - Sağlık durumu (isteğe bağlı)
   - Davranış notları (isteğe bağlı)

### 3. Ses Analizi Yapma

1. "Ses Analizi" sayfasına gidin
2. Evcil hayvanınızı seçin
3. Sesin kaydedildiği durumu belirtin (isteğe bağlı ama önerilir)
4. Ses dosyası yükleyin veya canlı kaydedin
5. "Ses Analizi Yap" butonuna tıklayın
6. Analiz tamamlandığında sonuçları görüntüleyin

### 4. Analiz Sonuçlarını Görüntüleme

1. "Analiz Geçmişi" sayfasından önceki analizlerinizi görüntüleyin
2. İlgili analize tıklayarak detaylı sonuçları inceleyin
3. Spektrogramı ve AI analiz sonuçlarını görün
4. PDF rapor oluşturun veya sonuçları paylaşın

## 🔧 Yönetici İşlemleri

### Yönetici Girişi

Varsayılan yönetici hesabı:
- Kullanıcı adı: `admin`
- Şifre: `admin123`

### Yönetici Paneli Özellikleri

1. **Kullanıcı Yönetimi**
   - Kullanıcıları listeleme
   - Kullanıcıları aktif/pasif yapma
   - Kullanıcı bilgilerini görüntüleme

2. **Abonelik Planları**
   - Planları listeleme
   - Yeni plan ekleme
   - Plan düzenleme

3. **Sistem Ayarları**
   - Sistem ayarlarını görüntüleme ve düzenleme

## 🎛️ API Kullanımı

Uygulama aynı zamanda bir REST API sağlar. API dökümantasyonu için `http://localhost:5000/api/docs` adresini ziyaret edin.

## 🧪 Testlerin Çalıştırılması

Tüm testleri çalıştırmak için:

```bash
python run_tests.py
```

## 📊 Geliştirme

### Proje Yapısı

```
petvoice/
├── app/                 # Ana uygulama paketi
│   ├── __init__.py      # Uygulama başlatıcısı
│   ├── models/          # Veritabanı modelleri
│   ├── views/           # View fonksiyonları
│   ├── templates/       # HTML şablonları
│   ├── static/          # Statik dosyalar
│   └── utils/           # Yardımcı fonksiyonlar
├── migrations/          # Veritabanı migration'ları
├── tests/               # Test dosyaları
├── config.py            # Yapılandırma ayarları
├── requirements.txt     # Bağımlılıklar
└── run.py               # Uygulama başlatıcı
```

### Yeni Özellik Ekleme

1. Yeni bir view eklemek için `app/views/` dizinine yeni bir dosya oluşturun
2. Yeni bir model eklemek için `app/models/models.py` dosyasını güncelleyin
3. Yeni bir şablon eklemek için `app/templates/` dizinine yeni bir HTML dosyası ekleyin
4. Gerekli bağımlılıkları `requirements.txt` dosyasına ekleyin

## 🆘 Sorun Giderme

### Yaygın Sorunlar

1. **"ModuleNotFoundError: No module named 'psycopg2'" hatası**
   - Çözüm: `pip install psycopg2-binary` komutunu çalıştırın

2. **Redis sunucusu bulunamadı hatası**
   - Çözüm: Redis'i yükleyin veya `redis-server` komutunu çalıştırın

3. **Google API anahtarı hatası**
   - Çözüm: Geçerli bir Google Gemini API anahtarı alın ve ortam değişkenine ekleyin

### Destek

Sorunlarla karşılaşırsanız, lütfen GitHub issues bölümünden yardım isteyin veya geliştirici belgelerini inceleyin.