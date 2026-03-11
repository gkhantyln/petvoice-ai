# verify_wav_conversion.py
# WAV dönüşümünü doğrulama

import os
import sys

def test_wav_conversion():
    """Test WAV conversion functionality"""
    print("WAV dönüşümü testi başlatılıyor...")
    
    try:
        # Ses işleme modülünü içe aktar
        sys.path.append('app')
        from app.utils.sound_processor import process_sound_file
        
        # Önceden oluşturulmuş bir MP3 dosyası varsa onu kullan
        test_files = ["test_sound.mp3", "test_audio.mp3"]
        mp3_file = None
        
        for file in test_files:
            if os.path.exists(file):
                mp3_file = file
                break
        
        if not mp3_file:
            print("Test için MP3 dosyası bulunamadı.")
            print("Lütfen önce bir MP3 dosyası oluşturun.")
            return
        
        print(f"MP3 dosyası işleniyor: {mp3_file}")
        processed_data = process_sound_file(mp3_file)
        
        print("İşleme sonucu:")
        print(f"  - Örnek hızı: {processed_data['sample_rate']} Hz")
        print(f"  - Süre: {processed_data['duration']:.2f} saniye")
        print(f"  - Veri boyutu: {len(processed_data['data'])} örnek")
        print(f"  - Çıktı dosyası: {processed_data['file_path']}")
        
        # WAV dosyasının oluşturulup oluşturulmadığını kontrol et
        if processed_data['file_path'].endswith('.wav') and os.path.exists(processed_data['file_path']):
            print("✓ WAV dosyası başarıyla oluşturuldu")
            
            # AI analizi için dosya yolunun doğru olduğundan emin ol
            print(f"AI analizi için kullanılacak dosya: {processed_data['file_path']}")
            return processed_data['file_path']
        else:
            print("✗ WAV dosyası oluşturulamadı")
            return None
            
    except Exception as e:
        print(f"İşleme sırasında hata oluştu: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    wav_file = test_wav_conversion()
    if wav_file:
        print(f"\nArtık {wav_file} dosyasını AI analizi için kullanabilirsiniz.")
    else:
        print("\nWAV dönüşümü başarısız oldu.")