# test_mp3_processing.py
# MP3 işleme testi

import os
import sys
from pydub import AudioSegment
import numpy as np
from scipy.io.wavfile import write

def create_test_files():
    """Create test MP3 and WAV files"""
    print("Test dosyaları oluşturuluyor...")
    
    # Önce WAV dosyası oluştur
    duration = 3  # 3 saniye
    sample_rate = 44100
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    
    # 440 Hz frekansında bir sinüs dalgası (A notası)
    frequency = 440
    waveform = np.sin(2 * np.pi * frequency * t)
    
    # Dalga formunu normalize et ve 16-bit integer'a çevir
    waveform = waveform / np.max(np.abs(waveform))
    audio_data = np.int16(waveform * 32767)
    
    # WAV dosyasını yaz
    wav_filename = "test_audio.wav"
    write(wav_filename, sample_rate, audio_data)
    print(f"WAV dosyası oluşturuldu: {wav_filename}")
    
    # MP3 dosyasını oluştur
    try:
        # FFmpeg ayarlarını yap
        AudioSegment.ffmpeg = r"C:\ffmpeg\bin\ffmpeg.exe"
        
        # WAV dosyasını MP3'e çevir
        audio = AudioSegment.from_wav(wav_filename)
        mp3_filename = "test_audio.mp3"
        audio.export(mp3_filename, format="mp3")
        print(f"MP3 dosyası oluşturuldu: {mp3_filename}")
        
        return wav_filename, mp3_filename
    except Exception as e:
        print(f"MP3 dosyası oluşturulurken hata oluştu: {e}")
        return wav_filename, None

def test_sound_processing():
    """Test sound processing functionality"""
    print("\nSes işleme testi başlatılıyor...")
    
    # Test dosyalarını oluştur
    wav_file, mp3_file = create_test_files()
    
    if not mp3_file:
        print("MP3 dosyası oluşturulamadı, test sonlandırılıyor.")
        return
    
    try:
        # Ses işleme modülünü içe aktar
        sys.path.append('app')
        from app.utils.sound_processor import process_sound_file
        
        print(f"\nMP3 dosyası işleniyor: {mp3_file}")
        processed_data = process_sound_file(mp3_file)
        
        print("İşleme sonucu:")
        print(f"  - Örnek hızı: {processed_data['sample_rate']} Hz")
        print(f"  - Süre: {processed_data['duration']:.2f} saniye")
        print(f"  - Veri boyutu: {len(processed_data['data'])} örnek")
        print(f"  - Çıktı dosyası: {processed_data['file_path']}")
        
        # WAV dosyasının oluşturulup oluşturulmadığını kontrol et
        if processed_data['file_path'].endswith('.wav') and os.path.exists(processed_data['file_path']):
            print("✓ WAV dosyası başarıyla oluşturuldu")
        else:
            print("✗ WAV dosyası oluşturulamadı")
            
    except Exception as e:
        print(f"İşleme sırasında hata oluştu: {e}")
        import traceback
        traceback.print_exc()
    
    # Temizlik
    try:
        if os.path.exists(wav_file):
            os.remove(wav_file)
        if mp3_file and os.path.exists(mp3_file):
            os.remove(mp3_file)
        # Oluşturulan WAV dosyasını da sil
        if 'processed_data' in locals() and os.path.exists(processed_data['file_path']):
            os.remove(processed_data['file_path'])
    except:
        pass

if __name__ == "__main__":
    test_sound_processing()
    print("\nTest tamamlandı.")