import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

# Set the matplotlib backend before importing any matplotlib modules
import matplotlib
matplotlib.use('Agg')

import numpy as np
from utils.sound_processor import generate_interactive_spectrogram

# Create test data
sample_rate = 44100
duration = 5  # 5 seconds
t = np.linspace(0, duration, int(sample_rate * duration))
# Create a simple sine wave with varying frequency
data = np.sin(2 * np.pi * (440 + 220 * np.sin(2 * np.pi * 0.5 * t)) * t)

# Create output directory if it doesn't exist
output_dir = "test_output"
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, "app_test_spectrogram.png")

print("Testing app generate_interactive_spectrogram function...")
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