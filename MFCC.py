import librosa
import numpy as np
import pandas as pd

# Load the audio file
audio_file = r"C:\Users\cheon\Desktop\untitled.wav"
signal, sr = librosa.load(audio_file)

# Define the parameters for MFCC extraction
n_mfcc = 13
n_fft = 2048
hop_length = 512

# Split the audio signal into 1-second segments
segment_size = sr // hop_length
segments = len(signal) // (segment_size * hop_length)
signal = signal[:segments * segment_size * hop_length]
segments = np.array_split(signal, segments)

# Extract MFCC features for each segment
features = []
for segment in segments:
    mfccs = librosa.feature.mfcc(y=segment, sr=sr, n_mfcc=n_mfcc, n_fft=n_fft, hop_length=hop_length)
    features.append(mfccs.T)

# Save the features into a CSV file
features = np.vstack(features)
time_steps = np.arange(features.shape[0]) * hop_length / sr
header = ['time'] + [f'mfcc_{i}' for i in range(n_mfcc)]
df = pd.DataFrame(np.hstack((time_steps.reshape(-1, 1), features)), columns=header)
df.to_csv(r'C:/Users/{username}/Desktop/reviews11.csv', index=False)
import matplotlib.pyplot as plt

# Select a single segment
segment_idx = 0
segment = segments[segment_idx]

# Extract MFCC features for the segment
mfccs = librosa.feature.mfcc(y=segment, sr=sr, n_mfcc=n_mfcc, n_fft=n_fft, hop_length=hop_length)

# Plot the MFCC features
plt.figure(figsize=(10, 4))
librosa.display.specshow(mfccs, x_axis='time')
plt.colorbar()
plt.title(f'MFCCs for Segment {segment_idx}')
plt.tight_layout()
plt.show()