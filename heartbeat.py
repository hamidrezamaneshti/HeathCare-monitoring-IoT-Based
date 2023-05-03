import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import math
from scipy.interpolate import interp1d  # Import the interpolate function from SciPy

measures = {}


# Start Filtering
def get_data(filename):
    dataset = pd.read_csv(filename)
    return dataset


def rolmean(dataset, hrw, fs):
    mov_avg = dataset['hart'].rolling(int(hrw * fs)).mean()
    avg_hr = (np.mean(dataset.hart))
    mov_avg = [avg_hr if math.isnan(x) else x for x in mov_avg]
    mov_avg = [x * 1.2 for x in mov_avg]
    dataset['hart_rollingmean'] = mov_avg


def detect_peaks(dataset):
    window = []
    peaklist = []
    listpos = 0
    for datapoint in dataset.hart:
        rollingmean = dataset.hart_rollingmean[listpos]
        if (datapoint < rollingmean) and (len(window) < 1):
            listpos += 1
        elif (datapoint > rollingmean):
            window.append(datapoint)
            listpos += 1
        else:
            maximum = max(window)
            beatposition = listpos - len(window) + (window.index(max(window)))
            peaklist.append(beatposition)
            window = []
            listpos += 1
    measures['peaklist'] = peaklist
    measures['ybeat'] = [dataset.hart[x] for x in peaklist]


# End Filtering

def calc_RR(dataset, fs):
    peaklist = measures['peaklist']
    RR_list = []
    cnt = 0
    while (cnt < (len(peaklist) - 1)):
        RR_interval = (peaklist[cnt + 1] - peaklist[cnt])
        ms_dist = ((RR_interval / fs) * 1000.0)
        RR_list.append(ms_dist)
        cnt += 1
    RR_diff = []
    RR_sqdiff = []
    cnt = 0
    while (cnt < (len(RR_list) - 1)):
        RR_diff.append(abs(RR_list[cnt] - RR_list[cnt + 1]))
        RR_sqdiff.append(math.pow(RR_list[cnt] - RR_list[cnt + 1], 2))
        cnt += 1
    measures['RR_list'] = RR_list
    measures['RR_diff'] = RR_diff
    measures['RR_sqdiff'] = RR_sqdiff


def calc_ts_measures():
    RR_list = measures['RR_list']
    RR_diff = measures['RR_diff']
    RR_sqdiff = measures['RR_sqdiff']
    measures['bpm'] = 60000 / np.mean(RR_list)
    measures['ibi'] = np.mean(RR_list)
    measures['sdnn'] = np.std(RR_list)
    measures['sdsd'] = np.std(RR_diff)
    measures['rmssd'] = np.sqrt(np.mean(RR_sqdiff))
    NN20 = [x for x in RR_diff if (x > 20)]
    NN50 = [x for x in RR_diff if (x > 50)]
    measures['nn20'] = NN20
    measures['nn50'] = NN50
    measures['pnn20'] = float(len(NN20)) / float(len(RR_diff))
    measures['pnn50'] = float(len(NN50)) / float(len(RR_diff))


def plotter(dataset, title):
    peaklist = measures['peaklist']
    ybeat = measures['ybeat']
    # pltl
    plt.title(title)
    plt.plot(dataset.hart, alpha=0.5, color='blue', label="raw signal")
    plt.plot(dataset.hart_rollingmean, color='green', label="moving average")
    plt.scatter(peaklist, ybeat, color='red', label="average: %.1f BPM" % measures['bpm'])
    plt.legend(loc=4, framealpha=0.6)
    plt.show()


def process(dataset, hrw, fs):
    rolmean(dataset, hrw, fs)
    detect_peaks(dataset)
    calc_RR(dataset, fs)
    calc_ts_measures()
    plotter(dataset, "Heart rate")


def fr(dataset, fs):
    peaklist = measures['peaklist']  # First retrieve the lists we need
    RR_list = measures['RR_list']
    RR_x = peaklist[1:]  # Remove the first entry, because first interval is assigned to the second beat.
    RR_y = RR_list  # Y-values are equal to interval lengths
    RR_x_new = np.linspace(RR_x[0], RR_x[-1], RR_x[
        -1])  # Create evenly spaced timeline starting at the second peak, its endpoint and length equal to position of last peak
    f = interp1d(RR_x, RR_y, kind='cubic')  # Interpolate the signal with cubic spline interpolation
    print("F: ", f(250))
    # plt1
    plt.title("Original and Interpolated Signal")
    plt.plot(RR_x, RR_y, label="Original", color='blue')
    plt.plot(RR_x_new, f(RR_x_new), label="Interpolated", color='red')
    plt.legend()
    plt.show()
    # Set variables
    n = len(dataset.hart)  # Length of the signal
    frq = np.fft.fftfreq(len(dataset.hart), d=((1 / fs)))  # divide the bins into frequency categories
    frq = frq[range(int((n / 2)))]  # Get single side of the frequency range
    # Do FFT
    Y = np.fft.fft(f(RR_x_new)) / n  # Calculate FFT
    Y = Y[range(int((n / 2)))]  # Return one side of the FFT

    lf = np.trapz(abs(Y[(frq >= 0.04) & (
            frq <= 0.15)]))  # Slice frequency spectrum where x is between 0.04 and 0.15Hz (LF), and use NumPy's trapezoidal integration function to find the area
    print("LF:", lf)
    hf = np.trapz(abs(Y[(frq >= 0.16) & (frq <= 0.5)]))  # Do the same for 0.16-0.5Hz (HF)
    print("HF:", hf)

    # Plot
    plt.title("Frequency Spectrum of Heart Rate Variability")
    plt.xlim(0, 0.6)  # Limit X axis to frequencies of interest (0-0.6Hz for visibility, we are interested in 0.04-0.5)
    plt.ylim(0, 50)  # Limit Y axis for visibility
    plt.plot(frq, abs(Y))  # Plot it
    plt.xlabel("Frequencies in Hz")
    plt.show()
