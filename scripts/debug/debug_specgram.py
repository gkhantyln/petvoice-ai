import numpy as np
import matplotlib.mlab as mlab

# Create test data
sample_rate = 44100
duration = 5  # 5 seconds
t = np.linspace(0, duration, int(sample_rate * duration))
# Create a simple sine wave
data = np.sin(2 * np.pi * 440 * t)

print("Test data shape:", data.shape)

# Test specgram function
frequencies, times, Sxx = mlab.specgram(data, Fs=sample_rate, NFFT=1024, noverlap=512)

print("Frequencies shape:", frequencies.shape)
print("Times shape:", times.shape)
print("Sxx shape:", Sxx.shape)

# Let's understand what we're getting
print("\nDetailed analysis:")
print("frequencies is a 2D array with shape:", frequencies.shape)
print("times is a 1D array with shape:", times.shape)
print("Sxx is a 1D array with shape:", Sxx.shape)

# What we actually need for pcolormesh:
# X should be 1D array of times (length = number of time bins)
# Y should be 1D array of frequencies (length = number of frequency bins)
# C should be 2D array (number of frequency bins, number of time bins)

# Extract what we need:
# For a proper spectrogram, we need the frequency bins (usually the first column of frequencies)
freq_bins = frequencies[:, 0]  # First column should be the frequency values
time_bins = times  # This should be correct already

print("\nAfter processing:")
print("freq_bins shape:", freq_bins.shape)
print("time_bins shape:", time_bins.shape)
print("Sxx shape:", Sxx.shape)

# But Sxx is still 1D, which is wrong. Let's check if we're using the right function
print("\nLet's try using plt.specgram instead:")
import matplotlib.pyplot as plt
plt.figure()
Pxx, freqs, bins, im = plt.specgram(data, Fs=sample_rate, NFFT=1024, noverlap=512)
plt.close()

print("Using plt.specgram:")
print("Pxx shape:", Pxx.shape)
print("freqs shape:", freqs.shape)
print("bins shape:", bins.shape)