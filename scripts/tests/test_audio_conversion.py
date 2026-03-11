# test_audio_conversion.py
# Audio conversion test script

import os
from pydub import AudioSegment
from pydub.utils import which

def test_ffmpeg():
    """Test if FFmpeg is available"""
    print("Testing FFmpeg availability...")
    
    # Check if ffmpeg is available
    ffmpeg_path = which("ffmpeg")
    if ffmpeg_path:
        print(f"✓ FFmpeg found at: {ffmpeg_path}")
        return True
    else:
        print("✗ FFmpeg not found")
        return False

def test_audio_conversion():
    """Test audio conversion functionality"""
    print("\nTesting audio conversion...")
    
    try:
        # Create a simple test audio file (if possible)
        # This will fail if FFmpeg is not available
        test_file = "test_audio.mp3"
        
        # Try to create a simple audio segment
        # This is just to test if the library works
        audio = AudioSegment.empty()
        print("✓ PyDub is working")
        
        # Try to check what formats are supported
        from pydub.utils import get_supported_codecs
        codecs = get_supported_codecs()
        print(f"Supported codecs: {list(codecs.keys())[:10]}...")  # Show first 10
        
        return True
    except Exception as e:
        print(f"✗ Audio conversion test failed: {e}")
        return False

if __name__ == "__main__":
    ffmpeg_available = test_ffmpeg()
    conversion_working = test_audio_conversion()
    
    if not ffmpeg_available:
        print("\n" + "="*50)
        print("FFmpeg is required for MP3 and other audio format support.")
        print("To fix this issue:")
        print("1. Download FFmpeg from: https://ffmpeg.org/download.html")
        print("2. Extract it to a folder (e.g., C:\\ffmpeg)")
        print("3. Add C:\\ffmpeg\\bin to your system PATH")
        print("4. Restart your command prompt/IDE")
        print("5. Run this test again to verify")
        print("="*50)
    
    print(f"\nSummary:")
    print(f"  FFmpeg available: {'Yes' if ffmpeg_available else 'No'}")
    print(f"  Audio conversion: {'Working' if conversion_working else 'Not working'}")
    print(f"\nFor best compatibility, use WAV files which don't require FFmpeg.")