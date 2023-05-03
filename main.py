from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
import heartbeat as hb #Assuming we named the file 'heartbeat.py'
import math
import numpy as np
dataset = hb.get_data("ECG_MONITORING/Sample_Dataset.csv")
hb.process(dataset, 0.75, 100)
#We have imported our Python module as an object called 'hb'
#This object contains the dictionary 'measures' with all values in it
#Now we can also retrieve the BPM value (and later other values) like this:

hb.measures['bpm_avg']
hb.measures['ibi']
hb.measures['sdnn']
#To view all objects in the dictionary, use "keys()" like so:
print (hb.measures)

peaklist = hb.measures['peaklist']  # First retrieve the lists we need
RR_list = hb.measures['RR_list']
RR_x = peaklist[1:]  # Remove the first entry, because first interval is assigned to the second beat.
RR_y = RR_list  # Y-values are equal to interval lengths
RR_x_new = np.linspace(RR_x[0], RR_x[-1], RR_x[-1]) # Create evenly spaced timeline starting at the second peak, its endpoint and length equal to position of last peak
f = interp1d(RR_x, RR_y, kind='cubic')  # Interpolate the signal with cubic spline interpolation
print("FD: ",f(250))

plt.title("Original and Interpolated Signal")
plt.plot(RR_x, RR_y, label="Original", color='blue')
plt.plot(RR_x_new, f(RR_x_new), label="Interpolated", color='red')
plt.legend()
plt.show()


#Set variables
n = len(dataset.hart) #Length of the signal
frq = np.fft.fftfreq(len(dataset.hart), d=((1/hb.fs))) #divide the bins into frequency categories
n1=int(n/2)
frq = frq[range(n1)] #Get single side of the frequency range
#Do FFT
Y = np.fft.fft(f(RR_x_new))/n #Calculate FFT
Y = Y[range(n1)] #Return one side of the FFT
#Plot
plt.title("Frequency Spectrum of Heart Rate Variability")
plt.xlim(0,0.6) #Limit X axis to frequencies of interest (0-0.6Hz for visibility, we are interested in 0.04-0.5)
plt.ylim(0, 50) #Limit Y axis for visibility
plt.plot(frq, abs(Y)) #Plot it
plt.xlabel("Frequencies in Hz")
plt.show()

lf = np.trapz(abs(Y[(frq>=0.04) & (frq<=0.15)])) #Slice frequency spectrum where x is between 0.04 and 0.15Hz (LF), and use NumPy's trapezoidal integration function to find the area
print ("LF/ Short-term blood pressure:", lf)
hf = np.trapz(abs(Y[(frq>=0.16) & (frq<=0.5)])) #Do the same for 0.16-0.5Hz (HF)
print ("HF/ breathing rate:", hf)
