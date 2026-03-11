# test_ffmpeg_fix.py
# FFmpeg düzeltme testi

import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

def test_ffmpeg_fix():
    """Test if FFmpeg fix works"""
    print("FFmpeg düzeltme testi başlatılıyor...")
    
    try:
        # sound_processor modülünü içe aktar
        from app.utils.sound_processor import is_ffmpeg_available
        
        # FFmpeg kullanılabilirliğini kontrol et
        ffmpeg_available = is_ffmpeg_available()
        
        if ffmpeg_available:
            print("✓ FFmpeg kullanılabilir durumda")
            print("Artık MP3 ve diğer ses formatlarını da yükleyebilmelisiniz.")
        else:
            print("✗ FFmpeg hala bulunamadı")
            print("Lütfen FFmpeg'in C:\\ffmpeg\\bin dizininde kurulu olduğundan emin olun.")
            
    except Exception as e:
        print(f"Test sırasında hata oluştu: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_ffmpeg_fix()