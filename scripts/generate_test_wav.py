# generate_test_wav.py
# Test WAV dosyası oluşturucu

import numpy as np
from scipy.io.wavfile import write
import os

def generate_test_wav(filename="test_sound.wav", duration=5, sample_rate=44100):
    """
    Test amaçlı bir WAV dosyası oluşturur
    
    Args:
        filename (str): Oluşturulacak dosyanın adı
        duration (int): Ses dosyasının süresi (saniye)
        sample_rate (int): Örnekleme frekansı (Hz)
    """
    
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
    write(filename, sample_rate, audio_data)
    
    file_size = os.path.getsize(filename)
    print(f"Test WAV dosyası oluşturuldu: {filename}")
    print(f"Dosya boyutu: {file_size} byte ({file_size/1024:.2f} KB)")
    print(f"Süre: {duration} saniye")
    print(f"Örnekleme frekansı: {sample_rate} Hz")
    print(f"Frekanslar: {frequency} Hz ve {frequency2} Hz")

if __name__ == "__main__":
    generate_test_wav()
    print("\nArtık bu dosyayı PetVoice AI uygulamasına yükleyebilirsiniz.")
    print("WAV dosyaları FFmpeg gerektirmez ve doğrudan işlenebilir.")