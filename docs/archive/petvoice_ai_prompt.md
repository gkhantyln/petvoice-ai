# 🐾 PetVoice AI - Kapsamlı Web Platformu Geliştirme Promptu

## 🎯 Proje Özeti
Hayvan sahiplerinin evcil hayvanlarının seslerini analiz ederek duygusal durumlarını, ihtiyaçlarını ve sağlık durumlarını anlayabilecekleri **profesyonel bir web platformu** oluşturun. Platform, **Flask Python** ile geliştirilecek, **PostgreSQL 17.6.1** veritabanı kullanacak ve **Gemini AI** entegrasyonu ile güçlendirilecektir.

---

## 🏗️ Teknik Altyapı Gereksinimleri

### **Backend Framework ve Teknolojiler:**
- **Flask 3.0+** (Ana web framework)
- **Flask-SQLAlchemy** (ORM)
- **Flask-Login** (Kullanıcı oturumu yönetimi)
- **Flask-Mail** (E-posta servisleri)
- **Flask-Admin** (Yönetici paneli)
- **Flask-JWT-Extended** (API token yönetimi)
- **Flask-Migrate** (Veritabanı migration)
- **Celery + Redis** (Arka plan işlemleri)
- **PostgreSQL 17.6.1** (Ana veritabanı)
- **Redis** (Cache ve session storage)

### **AI ve Analiz Kütüphaneleri:**
- **google-generativeai** (Gemini AI)
- **librosa** (Gelişmiş ses analizi)
- **scipy** (Bilimsel hesaplamalar)
- **matplotlib/plotly** (Görselleştirme)
- **numpy** (Sayısal işlemler)
- **pandas** (Veri analizi)
- **tensorflow** (Gelecekte özel model için)

### **Frontend Teknolojileri:**
- **HTML5, CSS3, JavaScript ES6+**
- **Bootstrap 5** veya **Tailwind CSS**
- **Chart.js** (Grafik görselleştirme)
- **Web Audio API** (Ses kaydetme)
- **Font Awesome** (İkonlar)
- **AOS.js** (Animasyonlar)

---

## 🗄️ PostgreSQL Veritabanı Şeması

### **Kullanıcı Tabloları:**
```sql
-- Kullanıcılar tablosu
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    phone VARCHAR(20),
    country VARCHAR(50),
    city VARCHAR(100),
    subscription_type VARCHAR(20) DEFAULT 'free', -- free, premium, pro
    subscription_end_date TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    is_verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP,
    profile_image_url VARCHAR(255)
);

-- Evcil hayvan profilleri
CREATE TABLE pets (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL,
    species VARCHAR(50) NOT NULL, -- cat, dog, bird, etc.
    breed VARCHAR(100),
    age INTEGER,
    gender VARCHAR(10),
    weight DECIMAL(5,2),
    health_conditions TEXT,
    behavioral_notes TEXT,
    profile_image_url VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE
);

-- Ses kayıtları ve analizler
CREATE TABLE sound_analyses (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    pet_id INTEGER REFERENCES pets(id) ON DELETE CASCADE,
    unique_id VARCHAR(50) UNIQUE NOT NULL,
    original_filename VARCHAR(255),
    file_path VARCHAR(255) NOT NULL,
    file_size INTEGER,
    duration_seconds DECIMAL(6,2),
    sample_rate INTEGER,
    context_situation VARCHAR(100),
    custom_context TEXT,
    ai_analysis TEXT,
    confidence_score DECIMAL(5,2),
    emotion_detected VARCHAR(50),
    urgency_level VARCHAR(20), -- low, medium, high, emergency
    veterinary_recommendation TEXT,
    spectrogram_path VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    analysis_status VARCHAR(20) DEFAULT 'processing' -- processing, completed, failed
);

-- Analiz geçmişi istatistikleri
CREATE TABLE analysis_stats (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    pet_id INTEGER REFERENCES pets(id) ON DELETE CASCADE,
    analysis_date DATE,
    total_analyses INTEGER DEFAULT 0,
    emotion_breakdown JSONB, -- {"happy": 5, "stressed": 2, "hungry": 3}
    average_confidence DECIMAL(5,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### **Yönetici ve İş Tabloları:**
```sql
-- Yönetici kullanıcıları
CREATE TABLE admin_users (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    role VARCHAR(50) DEFAULT 'admin', -- admin, super_admin, moderator
    permissions JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Sistem ayarları
CREATE TABLE system_settings (
    id SERIAL PRIMARY KEY,
    setting_key VARCHAR(100) UNIQUE NOT NULL,
    setting_value TEXT,
    description TEXT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Abonelik planları
CREATE TABLE subscription_plans (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    price DECIMAL(8,2) NOT NULL,
    currency VARCHAR(3) DEFAULT 'USD',
    duration_months INTEGER DEFAULT 1,
    max_analyses_per_month INTEGER,
    features JSONB,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## 🎨 Profesyonel Web Tasarımı Özellikleri

### **Ana Sayfa (Landing Page) Gereksinimleri:**
- **Hero Section:** Etkileyici animasyonlu başlık, ses dalgası animasyonu
- **Özellik Showcase:** Interaktif özellik kartları
- **Demo Video:** Platform kullanımını gösteren 60 saniyelik video
- **Müşteri Testimonialları:** Gerçek kullanıcı yorumları
- **Fiyatlandırma Tablosu:** Şeffaf ve çekici abonelik planları
- **FAQ Bölümü:** Sık sorulan sorular
- **İletişim Formu:** Profesyonel iletişim seçenekleri

### **Kullanıcı Dashboard Özellikleri:**
- **Evcil Hayvan Kartları:** Her pet için özet bilgiler
- **Son Analizler:** Kronolojik analiz listesi
- **İstatistik Grafikleri:** Aylık/haftalık analiz trendleri
- **Hızlı Ses Kaydetme:** Tek tıkla kayıt başlatma
- **Bildirimler:** Önemli durumlar için alert sistemi
- **Profil Yönetimi:** Kullanıcı ve pet bilgileri düzenleme

### **Ses Analizi Arayüzü:**
- **Real-time Ses Kaydetme:** Web Audio API ile canlı kayıt
- **Drag & Drop Upload:** Kolay dosya yükleme
- **Spektrogram Görselleştirme:** Interaktif ses dalgası grafiği
- **Analiz Progress Bar:** Canlı analiz durumu
- **Sonuç Raporu:** Detaylı PDF rapor oluşturma
- **Sosyal Paylaşım:** Güvenli sonuç paylaşımı

---

## 🤖 Gelişmiş AI Entegrasyonu

### **Gemini AI Prompt Optimizasyonu:**
```python
def create_advanced_analysis_prompt(pet_data, context_data, audio_features):
    return f"""
    Sen veteriner hekim düzeyinde hayvan davranış uzmanısın. 
    
    HAYVAN BİLGİLERİ:
    - Tür: {pet_data.species}
    - Yaş: {pet_data.age} 
    - Cinsiyet: {pet_data.gender}
    - Sağlık Durumu: {pet_data.health_conditions}
    
    SES VERİLERİ:
    - Süre: {audio_features['duration']} saniye
    - Frekans Aralığı: {audio_features['frequency_range']}
    - Yoğunluk: {audio_features['intensity']}
    - Dominant Frekans: {audio_features['dominant_freq']} Hz
    
    BAĞLAM: {context_data}
    
    Lütfen şu başlıklar altında profesyonel analiz sun:
    1. Aciliyet Seviyesi (1-5 skala)
    2. Tespit Edilen Duygu Durumu
    3. Olası İhtiyaç veya Sorun
    4. Sahibe Tavsiyeler
    5. Veteriner Kontrolü Gerekip Gerekmediği
    6. Güven Skoru (0-100)
    
    Cevabını JSON formatında ver.
    """
```

### **Çoklu AI Model Desteği:**
- Primary: Gemini AI
- Backup: OpenAI GPT-4
- Custom: TensorFlow Lite özel model (gelecek)
- Ensemble: Çoklu model sonuçlarını birleştirme

---

## 🔐 Güvenlik ve Performans

### **Güvenlik Önlemleri:**
- **CSRF Protection** (Flask-WTF)
- **Rate Limiting** (Flask-Limiter)
- **SQL Injection** koruması
- **Dosya Upload** güvenliği
- **HTTPS** zorunluluğu
- **GDPR** uyumlu veri işleme
- **API Key** güvenliği

### **Performans Optimizasyonu:**
- **Database Indexing** (PostgreSQL)
- **Redis Caching** sistemi
- **CDN** entegrasyonu
- **Lazy Loading** (görseller için)
- **Compression** (ses dosyaları)
- **Background Tasks** (Celery)

---

## 📱 Responsive ve Modern UX/UI

### **Design System:**
- **Color Palette:** Pet-friendly renkler (#FF6B6B, #4ECDC4, #45B7D1, #96CEB4)
- **Typography:** Google Fonts (Poppins + Open Sans)
- **Component Library:** Yeniden kullanılabilir bileşenler
- **Animation:** Subtle micro-interactions
- **Accessibility:** WCAG 2.1 AA uyumluluğu

### **Mobile-First Approach:**
- Responsive breakpoints
- Touch-friendly interface
- Progressive Web App (PWA) özellikleri
- Offline capability (limited)

---

## 📊 Analytics ve Raporlama

### **Kullanıcı Analytics:**
- Google Analytics 4 entegrasyonu
- Custom event tracking
- Conversion funnel analizi
- Kullanıcı journey mapping

### **Business Intelligence:**
- Admin dashboard metrikleri
- Abonelik dönüşüm oranları
- Popüler özellik kullanımı
- AI analiz başarı oranları

---

## 🚀 Deployment ve DevOps

### **Production Environment:**
```bash
# Docker containerization
# PostgreSQL 17.6.1 cluster
# Redis cluster
# Nginx reverse proxy
# SSL/TLS sertifikası
# Backup stratejisi
# Monitoring (Prometheus + Grafana)
```

### **CI/CD Pipeline:**
- GitHub Actions
- Automated testing
- Staging environment
- Blue-green deployment

---

## 💡 Gelecek Özellikler (Phase 2)

### **Advanced Features:**
- **Machine Learning:** Özel trained models
- **IoT Integration:** Smart collar compatibility  
- **Veteriner Network:** Uzman doktor bağlantısı
- **Multi-language:** 10+ dil desteği
- **API Marketplace:** Third-party integrations
- **Mobile Apps:** iOS & Android native apps

---

## ✅ Başlangıç Checklist

### **Geliştirme Adımları:**
1. ✅ Virtual environment kurulumu
2. ✅ PostgreSQL 17.6.1 kurulumu ve konfigürasyonu
3. ✅ Flask app structure oluşturma
4. ✅ Database schema migration
5. ✅ Temel authentication sistemi
6. ✅ File upload ve processing
7. ✅ Gemini AI entegrasyonu
8. ✅ Frontend template geliştirme
9. ✅ Admin panel oluşturma
10. ✅ Testing ve debugging

---

## 🎯 Success Metrics

### **KPI'lar:**
- Kullanıcı kaydı oranı: >15%
- Aylık aktif kullanıcı: >70%
- Premium dönüşüm: >5%
- AI analiz doğruluğu: >85%
- Platform uptime: >99.9%

Bu prompt ile **enterprise-level** bir platform oluşturabilir, **seed yatırım** alabilir seviyede profesyonel bir ürün ortaya çıkarabilirsiniz. Hangi bölümden başlamak istediğinizi belirtin, detaylı kod örnekleri hazırlayayım!