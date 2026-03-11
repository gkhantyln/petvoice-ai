# Katkıda Bulunma Rehberi

PetVoice AI projesine katkıda bulunmak istediğiniz için teşekkür ederiz! Bu rehber, projeye nasıl katkıda bulunabileceğinizi açıklar.

## 🤝 Katkı Türleri

### 1. Hata Bildirimi
- GitHub Issues kullanarak hata bildirin
- Hatayı yeniden oluşturma adımlarını ekleyin
- Beklenen ve gerçekleşen davranışı açıklayın
- Ekran görüntüleri ekleyin (varsa)

### 2. Özellik Önerisi
- GitHub Issues'da "Feature Request" etiketi ile açın
- Özelliğin neden gerekli olduğunu açıklayın
- Mümkünse kullanım senaryoları ekleyin

### 3. Kod Katkısı
- Fork edin ve branch oluşturun
- Kodunuzu yazın ve test edin
- Pull Request açın

## 🔧 Geliştirme Ortamı Kurulumu

1. **Projeyi fork edin ve klonlayın**
```bash
git clone https://github.com/YOUR_USERNAME/petvoice-ai.git
cd petvoice-ai
```

2. **Sanal ortam oluşturun**
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

3. **Bağımlılıkları yükleyin**
```bash
pip install -r requirements.txt
```

4. **Veritabanını başlatın**
```bash
python scripts/setup/init_db.py
```

5. **Uygulamayı çalıştırın**
```bash
python run.py
```

## 📝 Kod Standartları

### Python Kod Stili
- PEP 8 standartlarına uyun
- Fonksiyonlar için docstring kullanın
- Anlamlı değişken isimleri kullanın
- Maksimum satır uzunluğu: 100 karakter

### Commit Mesajları
Conventional Commits formatını kullanın:

```
<tip>: <kısa açıklama>

[opsiyonel detaylı açıklama]

[opsiyonel footer]
```

**Tipler:**
- `feat`: Yeni özellik
- `fix`: Hata düzeltme
- `docs`: Dokümantasyon değişikliği
- `style`: Kod formatı (mantık değişikliği yok)
- `refactor`: Kod yeniden yapılandırma
- `test`: Test ekleme/düzeltme
- `chore`: Genel bakım işleri

**Örnekler:**
```
feat: Add voice recording feature
fix: Fix spectrogram generation error
docs: Update installation instructions
```

### Branch İsimlendirme
```
feature/feature-name
fix/bug-description
docs/documentation-update
refactor/code-improvement
```

## 🧪 Test

Değişikliklerinizi test edin:

```bash
# Tüm testleri çalıştır
python scripts/run_tests.py

# Belirli bir test dosyasını çalıştır
python -m pytest scripts/tests/test_specific.py
```

## 📋 Pull Request Süreci

1. **Branch oluşturun**
```bash
git checkout -b feature/amazing-feature
```

2. **Değişikliklerinizi yapın**
- Kod yazın
- Test ekleyin
- Dokümantasyonu güncelleyin

3. **Commit edin**
```bash
git add .
git commit -m "feat: Add amazing feature"
```

4. **Push edin**
```bash
git push origin feature/amazing-feature
```

5. **Pull Request açın**
- GitHub'da Pull Request oluşturun
- Açıklayıcı bir başlık ve açıklama yazın
- İlgili issue'ları bağlayın (varsa)

### Pull Request Kontrol Listesi

- [ ] Kod PEP 8 standartlarına uygun
- [ ] Testler yazıldı ve geçiyor
- [ ] Dokümantasyon güncellendi
- [ ] Commit mesajları anlamlı
- [ ] Değişiklikler test edildi
- [ ] Çakışma yok

## 🐛 Hata Bildirimi Şablonu

```markdown
**Hata Açıklaması**
Hatanın kısa ve net açıklaması.

**Yeniden Oluşturma Adımları**
1. '...' sayfasına git
2. '...' butonuna tıkla
3. '...' alanına '...' yaz
4. Hatayı gör

**Beklenen Davranış**
Ne olmasını bekliyordunuz?

**Ekran Görüntüleri**
Varsa ekran görüntüleri ekleyin.

**Ortam:**
- İşletim Sistemi: [örn. Windows 10]
- Python Sürümü: [örn. 3.9]
- Tarayıcı: [örn. Chrome 90]

**Ek Bilgi**
Başka eklemek istediğiniz bilgi.
```

## 💡 Özellik Önerisi Şablonu

```markdown
**Özellik Açıklaması**
Özelliğin kısa ve net açıklaması.

**Sorun**
Bu özellik hangi sorunu çözüyor?

**Önerilen Çözüm**
Özelliğin nasıl çalışmasını istiyorsunuz?

**Alternatifler**
Düşündüğünüz alternatif çözümler.

**Ek Bilgi**
Başka eklemek istediğiniz bilgi, mockup'lar, örnekler.
```

## 📚 Dokümantasyon

Dokümantasyon katkıları da çok değerlidir:

- README.md güncellemeleri
- Kod yorumları ve docstring'ler
- Kullanım örnekleri
- Tutorial'lar
- API dokümantasyonu

## 🎯 İyi İlk Katkılar

Projeye yeni başlayanlar için uygun issue'lar:

- `good first issue` etiketi ile işaretlenmiş issue'lar
- Dokümantasyon güncellemeleri
- Küçük hata düzeltmeleri
- Test yazma

## ❓ Sorular

Sorularınız için:

- GitHub Discussions kullanın
- Issue açın
- Email gönderin

## 📜 Davranış Kuralları

- Saygılı olun
- Yapıcı geri bildirim verin
- Farklı görüşlere açık olun
- Topluluk odaklı düşünün

## 🙏 Teşekkürler

Katkılarınız için teşekkür ederiz! Her katkı, projeyi daha iyi hale getirir.
