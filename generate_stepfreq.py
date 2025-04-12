import os
import pandas as pd
import numpy as np
from scipy import signal
from scipy.fftpack import fft, fftfreq
from scipy.stats import linregress
from datetime import datetime
import matplotlib.pyplot as plt
from multiprocessing import Pool

FOLDER = "subjects"
dateparse = lambda x: datetime.strptime(x[:-6], "%Y-%m-%d %H:%M:%S.%f")

def get_step_freq(data, time, a, b, avg_T):
    # apply filter on data
    filt_data = signal.filtfilt(b, a, data)

    # zero data to the best fit line
    fit = linregress(x=time, y=filt_data)
    line = fit.intercept + time*fit.slope
    zeroed_data = filt_data - line

    # apply FFT
    x_fft = fft(zeroed_data)
    pwr_density = np.abs(x_fft) ** 2
    step_freq = fftfreq(len(pwr_density), avg_T)
    pwr_density /= np.max(pwr_density)
    peaks, _ = signal.find_peaks(pwr_density, prominence=0.8)

    # Find the subject's avg step frequency via their prominent frequencies
    return np.average(np.abs(step_freq[peaks]), weights=pwr_density[peaks])


def get_freq_data(subject_file):
    print(subject_file)
    accelData = pd.read_csv(os.path.join(FOLDER, subject_file), index_col=0, parse_dates=['loggingTime.txt.'], date_format="%Y-%m-%d %H:%M:%S.%f %z")

    # convert time to seconds and normalize to first sample
    start_time = accelData['loggingTime.txt.'][0]
    accelData['time.ms'] = (accelData['loggingTime.txt.'] - start_time).dt.total_seconds() * 1000

    # find the time gap in the data that separates the subject's route A->B and B->A.
    # remove the route B->A, so we can work with one contiguous span of measurements rather than 2.

    T_ms: pd.Series = (accelData['time.ms'].shift(-1) - accelData['time.ms']).dropna()
    # Gap should be found if where the period is >1 second long
    gap_indices = T_ms[T_ms > 1000]
    if gap_indices.size:
        accelData = accelData.iloc[:gap_indices.index[0] + 1]
        T_ms = T_ms[:gap_indices.index[0] + 1]

    avg_T = np.average(T_ms) / 1000

    # Get params for low pass filter
    b, a = signal.butter(3, 0.1, btype='lowpass', analog=False)

    func = lambda data: get_step_freq(data, accelData['time.ms'].values, a, b, avg_T)
    return [subject_file,
            func(accelData['motionUserAccelerationX.G.'].values), 
            func(accelData['motionUserAccelerationY.G.'].values), 
            func(accelData['motionUserAccelerationZ.G.'].values),]


if not os.path.exists(FOLDER):
    print(f"Folder '{FOLDER}' does not exist.")
    exit()


metadata = pd.read_csv('FinalMatrix-Gait-Meta-Data - FinalMatrix.csv')
metadata = metadata.drop(columns=['subject_left_waist_session1', 'subject_left_waist_session2', 'subject_right_pocket_session2'])
metadata = metadata.rename(columns={'subject_right_pocket_session1': 'subject'})

N_PROCESSES = 4
with Pool(N_PROCESSES) as pool:
    files = os.listdir(FOLDER)
    data = pool.map(get_freq_data, files)
    df = pd.DataFrame(data, columns=['subject', "x_freq", "y_freq", "z_freq"]).set_index('subject')

metadata = metadata.join(df, on='subject')
metadata = metadata.dropna()
metadata.to_csv('metadata_stepfreq.csv', encoding='utf-8')
