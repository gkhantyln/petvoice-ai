import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import os
import json

def generate_interactive_spectrogram(data, sample_rate, output_path):
    """
    Ses verisinden interaktif spektrogram oluşturur ve kaydeder
    """
    try:
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
        plt.savefig(basic_path)
        plt.close()
        
        # JSON verisini de kaydet (interaktif kullanım için)
        spectrogram_data = {
            'times': bins.tolist(),
            'frequencies': freqs.tolist(),
            'Sxx': Pxx.tolist(),
            'sample_rate': sample_rate,
            'duration': len(data) / sample_rate
        }
        
        json_path = output_path.replace('.png', '.json')
        with open(json_path, 'w') as f:
            json.dump(spectrogram_data, f)
        
        return basic_path, json_path
    except Exception as e:
        print(f"Spektrogram oluşturma hatası: {e}")
        import traceback
        traceback.print_exc()
        # Hata durumunda varsayılan değerler döndür
        return None, None

# Create test data
sample_rate = 44100
duration = 5  # 5 seconds
t = np.linspace(0, duration, int(sample_rate * duration))
# Create a simple sine wave with varying frequency
data = np.sin(2 * np.pi * (440 + 220 * np.sin(2 * np.pi * 0.5 * t)) * t)

# Create output directory if it doesn't exist
output_dir = "test_output"
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, "test_spectrogram.png")

print("Testing generate_interactive_spectrogram function...")
try:
    basic_path, json_path = generate_interactive_spectrogram(data, sample_rate, output_path)
    print(f"Success! Basic spectrogram path: {basic_path}")
    print(f"JSON spectrogram path: {json_path}")
    
    # Check if files were created
    if basic_path and os.path.exists(basic_path):
        print(f"Basic spectrogram file created: {basic_path}")
    else:
        print("Basic spectrogram file not created")
        
    if json_path and os.path.exists(json_path):
        print(f"JSON spectrogram file created: {json_path}")
    else:
        print("JSON spectrogram file not created")
        
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()