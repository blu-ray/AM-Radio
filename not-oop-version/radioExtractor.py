import numpy as np
from matplotlib import pyplot as plt
import BaseBandFilter as bbf
import wave
from scipy.io import wavfile as wav
import os


def draw_filter_fourier_transform(filter, extention):
    impulse = np.zeros(extention)
    impulse[0] = 1
    filter_extended = np.convolve(filter, impulse)
    ffts = np.fft.fft(filter_extended)
    ffts = np.abs(ffts)
    n = np.arange(len(filter_extended))
    fig, ax = plt.subplots(1, 1)
    ax.plot(n, ffts)
    plt.show()

def draw_signal_fourier_transform(signal):
    ffts = np.fft.fft(signal)
    ffts = np.abs(ffts)
    n = np.arange(len(signal))
    fig, ax = plt.subplots(1, 1)
    ax.plot(n, ffts)
    plt.show()


###sample rate in kilohertz
rate = 480

###Carriers Frequency in kilohertz
ava_freq = 96
eghtesad_freq = 144
goftogo_freq = 192
farhang_freq = 240

#filter specifications
delta_w = 0.1 * np.pi  #Approximate width of main lobe in radians
error = 0.1  #peak approximation error


myf = open("..\\Data\\input.txt").readlines()
raw_signal = [int(x) for x in myf]
raw_signal = np.array(raw_signal)
print(len(raw_signal))
#draw_signal_fourier_transform(raw_signal)

htop = np.pi/240  #converting kilo hertz to radians
station = input("Which Station? 1.Ava 2.Eghtesad 3.Goftogo 4.Farhang\n")

if station == "1":
    carrier_freq = ava_freq
    filename = "ava.wav"
elif station == "2":
    carrier_freq = eghtesad_freq
    filename = "eghtesad.wav"
elif station == "3":
    carrier_freq = goftogo_freq
    filename = "goftogo.wav"
else:
    carrier_freq = farhang_freq
    filename = "farhang.wav"

start_cutoff = (carrier_freq - 24) * htop
end_cutoff = (carrier_freq + 24) * htop
channel_extractor_filter = bbf.BaseBandFilter(start_cutoff, end_cutoff, delta_w, error)
low_pass_filter = bbf.BaseBandFilter(0, 20*htop, delta_w, error)   #maybe we can tolerate more main lobes width for LPF. use 5delta_w
print(len(low_pass_filter.filter_best))

#draw_filter_fourier_transform(channel_extractor_filter.filter_best, len(raw_signal)) #draw filter with the same dimension of main signal

channel_extracted_signal = np.convolve(raw_signal, channel_extractor_filter.filter_best)
n = np.arange(len(channel_extracted_signal))
#draw_signal_fourier_transform(channel_extracted_signal)

channel_extracted_signal_shifted = channel_extracted_signal * (np.cos(carrier_freq * htop * n))
#draw_signal_fourier_transform(channel_extracted_signal_shifted)

base_signal = np.convolve(channel_extracted_signal_shifted, low_pass_filter.filter_best)
n = np.arange(len(base_signal))
#draw_signal_fourier_transform(base_signal)

voice = [base_signal[10*x] for x in range(0,480000)]  #downsample
voice = np.array(voice)
wav.write(filename, 44100, voice.astype("int16"))
#draw_signal_fourier_transform(voice)

os.system("explorer " + filename)


