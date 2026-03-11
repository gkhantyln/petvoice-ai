# generate_test_mp3.py
# Test MP3 dosyası oluşturucu

import numpy as np
from scipy.io.wavfile import write
from pydub import AudioSegment
import os

def generate_test_mp3(filename="test_sound.mp3", duration=5, sample_rate=44100):
    """
    Test amaçlı bir MP3 dosyası oluşturur
    
    Args:
        filename (str): Oluşturulacak dosyanın adı
        duration (int): Ses dosyasının süresi (saniye)
        sample_rate (int): Örnekleme frekansı (Hz)
    """
    
    # Önce WAV dosyası oluştur
    wav_filename = filename.replace(".mp3", ".wav")
    
    # Zaman vektörünü oluştur
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    
    # Basit bir ses dalgası oluştur (440 Hz = A notası)
    frequency = 440  # Hz
    waveform = np.sin(2 * np.pi * frequency * t)
    
    # İkinci bir frekans ekleyelim (880 Hz)
    frequency2 = 880  # Hz
    waveform += 0.5 * np.sin(2 * np.pi * frequency2 * t)
    
    # Dalga formunu normalize et
    waveform = waveform / np.max(np.abs(waveform))
    
    # 16-bit signed integer'a çevir
    audio_data = np.int16(waveform * 32767)
    
    # WAV dosyasını yaz
    write(wav_filename, sample_rate, audio_data)
    
    # WAV dosyasını MP3'e çevir
    try:
        # FFmpeg'in tam yolunu belirt
        from pydub import AudioSegment
        AudioSegment.ffmpeg = r"C:\ffmpeg\bin\ffmpeg.exe"
        
        # WAV dosyasını yükle ve MP3 olarak kaydet
        audio = AudioSegment.from_wav(wav_filename)
        audio.export(filename, format="mp3")
        
        # WAV dosyasını sil
        os.remove(wav_filename)
        
        file_size = os.path.getsize(filename)
        print(f"Test MP3 dosyası oluşturuldu: {filename}")
        print(f"Dosya boyutu: {file_size} byte ({file_size/1024:.2f} KB)")
        print(f"Süre: {duration} saniye")
        print(f"Örnekleme frekansı: {sample_rate} Hz")
        print(f"Frekanslar: {frequency} Hz ve {frequency2} Hz")
        return True
    except Exception as e:
        print(f"MP3 dosyası oluşturulurken hata oluştu: {e}")
        # WAV dosyasını silmeyi deneyin
        if os.path.exists(wav_filename):
            os.remove(wav_filename)
        return False

if __name__ == "__main__":
    if generate_test_mp3():
        print("\nArtık bu dosyayı PetVoice AI uygulamasına yükleyebilirsiniz.")
        print("MP3 dosyaları artık doğru şekilde işlenebilmelidir.")
    else:
        print("\nMP3 dosyası oluşturulamadı.")
        print("Lütfen FFmpeg'in doğru şekilde yüklü olduğundan emin olun.")