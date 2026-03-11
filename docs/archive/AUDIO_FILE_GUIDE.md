# Ses Dosyası Yükleme Rehberi

Bu rehber, PetVoice AI uygulamasına ses dosyası yükleme konusunda size yardımcı olacak bilgileri içerir.

## Desteklenen Dosya Formatları

### 1. WAV (Önerilen)
- **Avantajlar**: 
  - FFmpeg gerektirmez
  - Doğrudan işlenir
  - En iyi uyumluluk
- **Önerilen kullanım**: İlk testleriniz için WAV dosyaları kullanın

### 2. MP3, OGG, FLAC
- **Gereksinimler**: FFmpeg'in sisteminizde yüklü olması
- **Not**: Şu anda sisteminizde FFmpeg bulunamadı

## Sorun Giderme

### "Sistem belirtilen dosyayı bulamıyor" hatası

Bu hata genellikle iki nedenden dolayı oluşur:

1. **FFmpeg eksikliği**: MP3, OGG veya FLAC dosyalarını işlemek için FFmpeg gerekir
2. **Dosya yolu sorunları**: Windows'ta dosya yollarıyla ilgili uyumsuzluklar

### Çözüm Önerileri

#### 1. WAV Dosyası Kullanma (En Kolay Çözüm)
- Test amaçlı oluşturulan [test_sound.wav](file://c:/Users/user/Desktop/AnimalsVoice/test_sound.wav) dosyasını kullanabilirsiniz
- Bu dosya doğrudan işlenebilir, FFmpeg gerektirmez

#### 2. FFmpeg Kurulumu
FFmpeg'i yüklemek isterseniz:

1. [https://ffmpeg.org/download.html](https://ffmpeg.org/download.html) adresinden FFmpeg'i indirin
2. Arşivi bir klasöre (örneğin `C:\ffmpeg`) çıkarın
3. `C:\ffmpeg\bin` klasörünü sistem PATH değişkenine ekleyin:
   - Windows arama çubuğuna "Environment Variables" yazın
   - "Edit the system environment variables" seçeneğine tıklayın
   - "Environment Variables" butonuna tıklayın
   - "System variables" bölümünden "Path" seçeneğini seçin ve "Edit" butonuna tıklayın
   - "New" butonuna tıklayıp `C:\ffmpeg\bin` yolunu ekleyin
   - "OK" butonlarına tıklayarak tüm pencereleri kapatın
4. Komut istemini yeniden başlatın
5. `ffmpeg -version` komutu ile kurulumu doğrulayın

## Test İşlemi

1. PetVoice AI uygulamasını başlatın
2. "Ses Analizi Yap" sayfasına gidin
3. Bir evcil hayvan seçin
4. WAV dosyasını yükleyin
5. Analiz işlemini başlatın

## Dosya Boyutu ve Süre Sınırlamaları

- **Maksimum dosya boyutu**: 16 MB
- **Önerilen süre**: 30 saniyeden kısa ses örnekleri
- **Format**: Mono veya stereo desteklenir (stereo dosyalar mono'ya çevrilir)

## En İyi Sonuçlar İçin İpuçları

1. **Sessiz ortamda** kayıt yapın
2. **Hayvanınızın doğal seslerini** kaydedin
3. **Kısa ve net** ses örnekleri tercih edin (5-10 saniye)
4. **Arka plan gürültüsünü** en aza indirin
5. **WAV formatı** kullanarak en iyi sonuçları alın

## Teknik Bilgiler

- Ses dosyaları `uploads/sounds` klasörüne kaydedilir
- Spektrogramlar `uploads/spectrograms` klasörüne kaydedilir
- Tüm dosya yolları Windows uyumluluğu için mutlak yollar olarak işlenir
- WAV dosyaları doğrudan işlenir, diğer formatlar önce WAV'e çevrilir