# app/utils/sound_processor.py
# Ses dosyası işleme yardımcı fonksiyonları
# Bu dosya, ses dosyalarının işlenmesi ve spektrogram oluşturulması işlemlerini içerir

import numpy as np
from scipy.io import wavfile
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import os
from pydub import AudioSegment
from pydub.utils import which

def is_ffmpeg_available():
    """Check if FFmpeg is available on the system"""
    # Önce sistemde FFmpeg olup olmadığını kontrol et
    ffmpeg_path = which("ffmpeg")
    if ffmpeg_path:
        return True
    
    # Windows'ta doğrudan C:\ffmpeg\bin\ffmpeg.exe yolunu kontrol et
    if os.name == 'nt':  # Windows
        windows_ffmpeg_path = r"C:\ffmpeg\bin\ffmpeg.exe"
        if os.path.exists(windows_ffmpeg_path):
            # PyDub'a FFmpeg yolunu bildir
            from pydub import AudioSegment
            AudioSegment.ffmpeg = windows_ffmpeg_path
            
            # Ortam değişkenlerini ayarla
            os.environ["PATH"] += os.pathsep + r"C:\ffmpeg\bin"
            os.environ["FFMPEG_PATH"] = windows_ffmpeg_path
            
            return True
    
    return False

def convert_to_wav(file_path):
    """
    Ses dosyasını WAV formatına dönüştürür
    """
    # Normalize file path for Windows
    file_path = os.path.abspath(file_path)
    
    # Dosya uzantısını al
    file_extension = os.path.splitext(file_path)[1].lower()
    
    # Zaten WAV ise olduğu gibi döndür
    if file_extension == '.wav':
        return file_path
    
    # FFmpeg kontrolü
    if not is_ffmpeg_available():
        raise RuntimeError("FFmpeg gerekli ancak sistemde bulunamadı. Lütfen FFmpeg'i yükleyin veya doğrudan WAV dosyası kullanın.")
    
    # Diğer formatları WAV'a dönüştür
    try:
        audio = AudioSegment.from_file(file_path, format=file_extension[1:])
        wav_path = file_path.rsplit('.', 1)[0] + '.wav'
        # Normalize output path for Windows
        wav_path = os.path.abspath(wav_path)
        audio.export(wav_path, format='wav')
        
        return wav_path
    except Exception as e:
        print(f"Dosya dönüştürme hatası: {e}")
        raise

def process_sound_file(file_path):
    """
    Ses dosyasını işler ve temel bilgileri döndürür
    """
    # Normalize file path for Windows
    file_path = os.path.abspath(file_path)
    
    # WAV formatına dönüştür
    try:
        wav_path = convert_to_wav(file_path)
    except RuntimeError as e:
        # FFmpeg yoksa doğrudan WAV dosyası kullanılmaya çalışılmış olabilir
        if os.path.splitext(file_path)[1].lower() == '.wav':
            wav_path = file_path
        else:
            raise e
    
    # Ses dosyasını oku
    sample_rate, data = wavfile.read(wav_path)
    
    # Stereo ise mono'ya çevir
    if data.ndim > 1:
        data = data.mean(axis=1)
    
    # Temel bilgileri hesapla
    duration = len(data) / sample_rate
    
    return {
        'data': data,
        'sample_rate': sample_rate,
        'duration': duration,
        'file_path': wav_path
    }

def generate_spectrogram(data, sample_rate, output_path):
    """
    Ses verisinden spektrogram oluşturur ve kaydeder
    """
    # Normalize output path for Windows
    output_path = os.path.abspath(output_path)
    
    plt.figure(figsize=(10, 4))
    plt.specgram(data, Fs=sample_rate, NFFT=1024, noverlap=512, cmap='inferno')
    plt.title("Hayvan Sesi Spektrogramı")
    plt.xlabel("Zaman (saniye)")
    plt.ylabel("Frekans (Hz)")
    plt.colorbar(label='Yoğunluk (dB)')
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()
    
    return output_path

def generate_interactive_spectrogram(data, sample_rate, output_path):
    """
    Ses verisinden interaktif spektrogram oluşturur ve kaydeder
    """
    try:
        # Normalize output path for Windows
        output_path = os.path.abspath(output_path)
        
        # Spektrogram verisini hesapla
        # Use plt.specgram instead of mlab.specgram for correct parameter order
        Pxx, freqs, bins, im = plt.specgram(data, Fs=sample_rate, NFFT=1024, noverlap=512)
        
        # Log ölçeğine çevir
        Pxx = 10 * np.log10(Pxx)
        
        # Spektrogramı oluştur
        plt.figure(figsize=(12, 6))
        # Create proper meshgrid for pcolormesh
        T, F = np.meshgrid(bins, freqs)
        plt.pcolormesh(T, F, Pxx, cmap='inferno', shading='gouraud')
        plt.title("Hayvan Sesi Spektrogramı")
        plt.xlabel("Zaman (saniye)")
        plt.ylabel("Frekans (Hz)")
        plt.colorbar(label='Yoğunluk (dB)')
        
        # Zaman ve frekans çizgileri ekle
        plt.grid(True, alpha=0.3)
        
        # PNG olarak kaydet
        plt.tight_layout()
        basic_path = output_path.replace('.png', '_basic.png')
        # Normalize path for Windows
        basic_path = os.path.abspath(basic_path)
        plt.savefig(basic_path)
        plt.close()
        
        # JSON verisini de kaydet (interaktif kullanım için)
        import json
        spectrogram_data = {
            'times': bins.tolist(),
            'frequencies': freqs.tolist(),
            'Sxx': Pxx.tolist(),
            'sample_rate': sample_rate,
            'duration': len(data) / sample_rate
        }
        
        json_path = output_path.replace('.png', '.json')
        # Normalize path for Windows
        json_path = os.path.abspath(json_path)
        with open(json_path, 'w') as f:
            json.dump(spectrogram_data, f)
        
        return basic_path, json_path
    except Exception as e:
        print(f"Spektrogram oluşturma hatası: {e}")
        import traceback
        traceback.print_exc()
        # Hata durumunda varsayılan değerler döndür
        return None, None

def get_audio_features(data, sample_rate):
    """
    Ses verisinden temel özellikleri çıkarır
    """
    # Süre
    duration = len(data) / sample_rate
    
    # Frekans aralığı
    freq_range = (0, sample_rate / 2)
    
    # Yoğunluk (RMS)
    rms = np.sqrt(np.mean(data**2))
    
    # Dominant frekans
    fft = np.fft.fft(data)
    freqs = np.fft.fftfreq(len(data), 1/sample_rate)
    dominant_freq = abs(freqs[np.argmax(np.abs(fft))])
    
    return {
        'duration': duration,
        'frequency_range': freq_range,
        'intensity': float(rms),
        'dominant_freq': float(dominant_freq)
    }