# 🔄 Multi-Provider AI Sistemi Kullanım Kılavuzu

PetVoice AI, birden fazla AI provider'ı destekler ve otomatik failover mekanizması ile kesintisiz hizmet sağlar.

## 🎯 Özellikler

### Desteklenen Provider'lar

1. **Google Gemini** (Varsayılan)
   - Model: gemini-2.5-flash
   - Ses analizi desteği
   - Hızlı ve güvenilir

2. **OpenAI GPT-4** (Opsiyonel)
   - Model: gpt-4o-audio-preview
   - Gelişmiş ses analizi
   - Yüksek kalite

3. **Anthropic Claude** (Opsiyonel)
   - Model: claude-3-5-sonnet
   - Detaylı analiz
   - Güvenli ve etik

### Failover Mekanizması

Sistem, bir provider başarısız olduğunda otomatik olarak sıradaki provider'ı dener:

```
Gemini (Ana) → OpenAI (Yedek 1) → Claude (Yedek 2)
```

## 📝 Yapılandırma

### 1. Temel Yapılandırma

`.env` dosyasında en az bir provider yapılandırın:

```env
# Google Gemini (Zorunlu)
GOOGLE_API_KEY=your_gemini_api_key_here
```

### 2. Çoklu Provider Yapılandırması

Birden fazla provider ekleyin:

```env
# Google Gemini
GOOGLE_API_KEY=your_gemini_api_key_here

# OpenAI (Opsiyonel)
OPENAI_API_KEY=your_openai_api_key_here

# Anthropic Claude (Opsiyonel)
ANTHROPIC_API_KEY=your_anthropic_api_key_here
```

### 3. Çoklu API Anahtarı (Failover)

Her provider için birden fazla API anahtarı ekleyin:

```env
# Google Gemini - Çoklu Anahtar
GOOGLE_API_KEY=primary_gemini_key
GOOGLE_API_KEY_1=backup_gemini_key_1
GOOGLE_API_KEY_2=backup_gemini_key_2

# OpenAI - Çoklu Anahtar
OPENAI_API_KEY=primary_openai_key
OPENAI_API_KEY_1=backup_openai_key_1

# Anthropic - Çoklu Anahtar
ANTHROPIC_API_KEY=primary_claude_key
ANTHROPIC_API_KEY_1=backup_claude_key_1
```

## 🔑 API Anahtarı Alma

### Google Gemini

1. [Google AI Studio](https://aistudio.google.com/app/apikey) adresine gidin
2. "Create API Key" butonuna tıklayın
3. Anahtarı kopyalayın ve `.env` dosyasına ekleyin

### OpenAI

1. [OpenAI Platform](https://platform.openai.com/api-keys) adresine gidin
2. "Create new secret key" butonuna tıklayın
3. Anahtarı kopyalayın ve `.env` dosyasına ekleyin
4. OpenAI kütüphanesini yükleyin:
   ```bash
   pip install openai
   ```

### Anthropic Claude

1. [Anthropic Console](https://console.anthropic.com/) adresine gidin
2. API anahtarı oluşturun
3. Anahtarı kopyalayın ve `.env` dosyasına ekleyin
4. Anthropic kütüphanesini yükleyin:
   ```bash
   pip install anthropic
   ```

## 🚀 Kullanım

### Otomatik Failover

Sistem otomatik olarak çalışır. Kod değişikliği gerekmez:

```python
# Eski kod (hala çalışır)
result = analyze_with_gemini(audio_path, pet_id, context, custom_context)

# Sistem otomatik olarak:
# 1. Gemini'yi dener
# 2. Başarısız olursa OpenAI'yi dener
# 3. O da başarısız olursa Claude'u dener
```

### Provider Durumunu Kontrol Etme

Admin panelinden provider durumunu görüntüleyin:

```
http://localhost:5000/admin/ai-providers
```

### Programatik Kontrol

```python
from app.utils.ai_providers import get_ai_manager

manager = get_ai_manager()

# Kullanılabilir provider'ları listele
providers = manager.get_available_providers()
print(f"Kullanılabilir: {providers}")

# Durum bilgisi al
status = manager.get_provider_status()
print(f"Toplam: {status['total']}")
print(f"Aktif: {status['active']}")
print(f"Şu an kullanılan: {status['current']}")
```

## 📊 Öncelik Sırası

Provider'lar şu sırayla denenir:

1. **Google Gemini** (Tüm anahtarlar)
   - GOOGLE_API_KEY
   - GOOGLE_API_KEY_1
   - GOOGLE_API_KEY_2
   - ...

2. **OpenAI** (Tüm anahtarlar)
   - OPENAI_API_KEY
   - OPENAI_API_KEY_1
   - ...

3. **Anthropic Claude** (Tüm anahtarlar)
   - ANTHROPIC_API_KEY
   - ANTHROPIC_API_KEY_1
   - ...

## 🔍 Hata Ayıklama

### Provider Durumunu Kontrol Etme

Uygulama başlatıldığında konsola şu mesajlar yazdırılır:

```
✓ Gemini Provider #1 aktif
✓ Gemini Provider #2 aktif
✓ OpenAI Provider #1 aktif
🎯 Aktif Provider: Google Gemini
```

### Analiz Sırasında

Analiz yapılırken hangi provider'ın kullanıldığını görebilirsiniz:

```
🔄 Google Gemini ile analiz deneniyor...
✓ Google Gemini ile analiz başarılı!
```

Veya failover durumunda:

```
🔄 Google Gemini ile analiz deneniyor...
✗ Google Gemini: API key not valid
🔄 OpenAI ile analiz deneniyor...
✓ OpenAI ile analiz başarılı!
```

### Yaygın Sorunlar

**Hiçbir provider yapılandırılmamış:**
```
⚠️ Hiçbir AI provider yapılandırılamadı!
```
**Çözüm:** En az bir geçerli API anahtarı ekleyin.

**Tüm provider'lar başarısız:**
```
Tüm AI provider'lar başarısız oldu
```
**Çözüm:** 
- API anahtarlarını kontrol edin
- İnternet bağlantınızı kontrol edin
- API kotalarınızı kontrol edin

## 💡 En İyi Uygulamalar

### 1. Çoklu Anahtar Kullanın

Her provider için en az 2 API anahtarı kullanın:

```env
GOOGLE_API_KEY=primary_key
GOOGLE_API_KEY_1=backup_key
```

### 2. Farklı Provider'lar Kullanın

Maksimum güvenilirlik için farklı provider'lar ekleyin:

```env
GOOGLE_API_KEY=gemini_key
OPENAI_API_KEY=openai_key
```

### 3. Kota Yönetimi

- Her API anahtarı için kota limitlerini takip edin
- Yedek anahtarlar için farklı hesaplar kullanın
- Düzenli olarak kota durumunu kontrol edin

### 4. Maliyet Optimizasyonu

Provider'ları maliyet açısından sıralayın:

1. Google Gemini (Ücretsiz/Düşük maliyet)
2. OpenAI (Orta maliyet)
3. Anthropic (Yüksek kalite, yüksek maliyet)

## 🔒 Güvenlik

### API Anahtarlarını Koruma

- API anahtarlarını asla kodda saklamayın
- `.env` dosyasını `.gitignore`'a ekleyin
- Production'da ortam değişkenlerini kullanın
- Anahtarları düzenli olarak yenileyin

### Rate Limiting

Her provider'ın kendi rate limit'i vardır:

- **Gemini:** 60 istek/dakika (ücretsiz)
- **OpenAI:** Hesap tipine göre değişir
- **Claude:** Hesap tipine göre değişir

## 📈 Performans

### Önbellekleme

Sistem, aynı ses için tekrar analiz yapmaz:

```python
# İlk analiz: API çağrısı yapılır
result1 = analyze_with_gemini(audio_path, ...)

# İkinci analiz: Önbellekten döner
result2 = analyze_with_gemini(audio_path, ...)  # Hızlı!
```

### Yanıt Süreleri

Ortalama yanıt süreleri:

- **Gemini:** 2-5 saniye
- **OpenAI:** 3-7 saniye
- **Claude:** 4-8 saniye

## 🆘 Destek

Sorun yaşıyorsanız:

1. Admin panelinden provider durumunu kontrol edin
2. Konsol loglarını inceleyin
3. API anahtarlarını doğrulayın
4. [GitHub Issues](https://github.com/kullaniciadi/petvoice-ai/issues) açın

---

**Multi-provider sistemi ile kesintisiz hizmet! 🚀**
