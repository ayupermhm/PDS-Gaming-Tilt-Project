import pandas as pd
import numpy as np

# Load CSV file
df = pd.read_csv(r"{path}", skiprows=1)

gsr = df['GSR']
time = df['Time']

# Calculate time difference in seconds
time_diff = np.diff(time)

# Calculate time interval in seconds
time_interval = time.iloc[1] - time.iloc[0]

# Calculate number of samples in a 1-second window
window_size = int(1 / time_interval) * 2

# Initialize lists to store calculated values
amplitude = []
scr_amplitude = []
latency = []
rise_time = []
time_reading = []

# Iterate over rolling window every 1 second
for i in range(0, len(gsr), window_size):
    # Extract data within 6-second window
    window_gsr = gsr[i:i + window_size]
    window_time = time[i:i + window_size]

    if len(window_gsr) > 0:
        # Calculate amplitude
        amp = np.max(window_gsr) - np.min(window_gsr)
        amplitude.append(amp)

        # Calculate SCR amplitude
        scr_amp = np.max(window_gsr) - window_gsr.iloc[0]
        scr_amplitude.append(scr_amp)

        # Calculate latency
        lat = window_time.iloc[np.argmax(window_gsr)] - window_time.iloc[0]
        latency.append(lat)

        # Calculate rise time
        rise_t = window_time.iloc[np.argmax(window_gsr)] - window_time.iloc[np.argmin(window_gsr)]
        rise_time.append(rise_t)

        # Store time of the reading
        time_reading.append(window_time.iloc[0])

# Convert lists to arrays
amplitude = np.array(amplitude)
scr_amplitude = np.array(scr_amplitude)
latency = np.array(latency)
rise_time = np.array(rise_time)
time_reading = np.array(time_reading)

# Create a DataFrame to store the calculated values
results_df = pd.DataFrame({
    'Time': time_reading,
    'Amplitude': amplitude,
    'SCR Amplitude': scr_amplitude,
    'Latency': latency,
    'Rise Time': rise_time
})

# Export the DataFrame to a CSV file on desktop
results_df.to_csv(r'{path}', index=False)