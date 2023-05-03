from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
import heartbeat as hb  # Assuming we named the file 'heartbeat.py'
import math
import numpy as np

# Load dataset and process it
dataset = hb.get_data("ECG_MONITORING/Sample_Dataset.csv")
hb.process(dataset, 0.75, 100)

# Retrieve and print the measures from the processed data
hb.measures['bpm_avg']
hb.measures['ibi']
hb.measures['sdnn']
print(hb.measures)

# Interpolate the signal
peaklist = hb.measures['peaklist']
RR_list = hb.measures['RR_list']
RR_x = peaklist[1:]
RR_y = RR_list
RR_x_new = np.linspace(RR_x[0], RR_x[-1], RR_x[-1])
f = interp1d(RR_x, RR_y, kind='cubic')
print("FD: ", f(250))

# Plot original and interpolated signal
plt.title("Original and Interpolated Signal")
plt.plot(RR_x, RR_y, label="Original", color='blue')
plt.plot(RR_x_new, f(RR_x_new), label="Interpolated", color='red')
plt.legend()
plt.show()

# Prepare for FFT
n = len(dataset.hart)
frq = np.fft.fftfreq(len(dataset.hart), d=((1/hb.fs)))
n1 = int(n/2)
frq = frq[range(n1)]

# Perform FFT and plot the frequency spectrum
Y = np.fft.fft(f(RR_x_new))/n
Y = Y[range(n1)]
plt.title("Frequency Spectrum of Heart Rate Variability")
plt.xlim(0, 0.6)
plt.ylim(0, 50)
plt.plot(frq, abs(Y))
plt.xlabel("Frequencies in Hz")
plt.show()

# Calculate LF and HF measures and print them
lf = np.trapz(abs(Y[(frq >= 0.04) & (frq <= 0.15)]))
print("LF/ Short-term blood pressure:", lf)
hf = np.trapz(abs(Y[(frq >= 0.16) & (frq <= 0.5)]))
print("HF/ breathing rate:", hf)
