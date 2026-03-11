# test_ai_with_wav.py
# WAV dosyası ile AI analizini test etme

import os
import sys

def test_ai_with_wav():
    """Test AI analysis with WAV file"""
    print("AI analizi testi başlatılıyor (WAV dosyası ile)...")
    
    try:
        # Ses işleme modülünü içe aktar
        sys.path.append('app')
        from app.utils.ai_analyzer import analyze_with_gemini
        
        # WAV dosyasını bul
        wav_files = ["test_sound.wav", "test_audio.wav"]
        wav_file = None
        
        for file in wav_files:
            if os.path.exists(file):
                wav_file = file
                break
        
        if not wav_file:
            print("Test için WAV dosyası bulunamadı.")
            print("Lütfen önce bir WAV dosyası oluşturun.")
            return
        
        print(f"WAV dosyası analiz ediliyor: {wav_file}")
        
        # AI analizini yap (test verileri ile)
        # Gerçek bir veritabanı bağlantısı olmadığı için örnek veriler kullanıyoruz
        pet_id = 1  # Örnek pet ID
        context_situation = "Genel (Durum Belirtilmedi)"
        custom_context = ""
        
        result = analyze_with_gemini(wav_file, pet_id, context_situation, custom_context)
        
        print("AI analiz sonucu:")
        print(f"  - Analiz metni: {result.get('ai_analysis', 'Bulunamadı')[:100]}...")
        print(f"  - Güven skoru: {result.get('confidence_score', 'Bilinmiyor')}")
        print(f"  - Tespit edilen duygu: {result.get('emotion_detected', 'Bilinmiyor')}")
        print(f"  - Aciliyet seviyesi: {result.get('urgency_level', 'Bilinmiyor')}")
        
        if result.get('ai_analysis'):
            print("✓ AI analizi başarıyla tamamlandı")
            return True
        else:
            print("✗ AI analizi başarısız oldu")
            return False
            
    except Exception as e:
        print(f"AI analizi sırasında hata oluştu: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_ai_with_wav()
    if success:
        print("\nAI analizi düzgün çalışıyor. MP3 dosyaları da WAV'e dönüştürüldükten sonra analiz edilebilmeli.")
    else:
        print("\nAI analizinde sorunlar var.")