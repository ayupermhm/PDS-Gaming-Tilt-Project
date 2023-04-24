import pandas as pd
import numpy as np
import math

# read the data from csv file
df = pd.read_csv(r"C:\Users\cheon\Downloads\SensorData0.csv")

# convert time to seconds
time = df['Time'].values

# define function to calculate metrics
def calculate_metrics(data):
    mean = np.mean(data)
    max_val = np.max(data)
    min_val = np.min(data)
    std = np.std(data)
    energy = np.sum(np.square(data))
    RMS = np.sqrt(np.mean(np.square(data)))
    abs_area = np.sum(np.abs(data))
    jerk = np.sum(np.abs(np.diff(data)))
    return {'mean': mean, 'max': max_val, 'min': min_val, 'std': std, 'energy': energy,'RMS': RMS, 'abs_area': abs_area, 'jerk': jerk}

# calculate metrics for accelerometer data
accel_metrics = df.groupby(np.floor(df['Time'])).agg({'AccelX': calculate_metrics, 'AccelY': calculate_metrics, 'AccelZ': calculate_metrics})
accel_metrics.columns = accel_metrics.columns.map('_'.join).str.strip()

# calculate metrics for gyroscope data
gyro_metrics = df.groupby(np.floor(df['Time'])).agg({'GyroX': np.mean, 'GyroY': np.mean, 'GyroZ': np.mean})
gyro_metrics.columns = gyro_metrics.columns.map(lambda x: x + '_mean').str.strip()

# merge accelerometer and gyroscope metrics
output = pd.concat([accel_metrics, gyro_metrics], axis=1)

# save output to csv file on desktop
output.to_csv(r'C:\Users\Cheon\Desktop\output1.csv', index=False)