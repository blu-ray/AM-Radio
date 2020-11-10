import numpy as np
from scipy import signal
from matplotlib import pyplot as plt


class BaseBandFilter:

    def __init__(self, w_start, w_end, delta_w, error):
        """
        :param w_start: frequency to start passing in radians (<pi)
        :param w_end: frequency to stop passing in radians (<pi)
        :param delta_w: Approximate width of main lobe in radians
        :param error: peak approximation error
        """
        error_db = 20 * np.log10(error)
        wc = (w_start - w_end)/2
        w_origin = (w_start + w_end)/2

        #Rectangular Filter
        window = self.rectangular(delta_w)
        m = len(window)
        l = int(m/2)
        n = np.arange(-l, l + 1, 1)
        n[l] = 1 #preventing divide by zero
        f = np.sin(wc * n) / (np.pi * n) #making low pass filter
        f = f * (np.cos(w_origin * n)) #moving filter to it's origin to get a band pass filter
        n[l] = 0
        f[l] = wc / np.pi
        self.filter_rect = f * window * 2


        #Bartlett Filter
        window = self.bartlett(delta_w)
        m = len(window)
        l = int(m/2)
        n = np.arange(-l, l + 1, 1)
        n[l] = 1 #preventing divide by zero
        f = np.sin(wc * n) / (np.pi * n) #making low pass filter
        f = f * (np.cos(w_origin * n)) #moving filter to it's origin to get a band pass filter
        n[l] = 0
        f[l] = wc / np.pi
        self.filter_bart = f * window * 2


        #Hann Filter
        window = self.hann(delta_w)
        m = len(window)
        l = int(m/2)
        n = np.arange(-l, l + 1, 1)
        n[l] = 1 #preventing divide by zero
        f = np.sin(wc * n) / (np.pi * n) #making low pass filter
        f = f * (np.cos(w_origin * n)) #moving filter to it's origin to get a band pass filter
        n[l] = 0
        f[l] = wc / np.pi
        self.filter_hann = f * window * 2


        #Hamming Filter
        window = self.hamming(delta_w)
        m = len(window)
        l = int(m/2)
        n = np.arange(-l, l + 1, 1)
        n[l] = 1 #preventing divide by zero
        f = np.sin(wc * n) / (np.pi * n) #making low pass filter
        f = f * (np.cos(w_origin * n)) #moving filter to it's origin to get a band pass filter
        n[l] = 0
        f[l] = wc / np.pi
        self.filter_hamm = f * window * 2


        #Blackman Filter
        window = self.blackman(delta_w)
        m = len(window)
        l = int(m/2)
        n = np.arange(-l, l + 1, 1)
        n[l] = 1 #preventing divide by zero
        f = np.sin(wc * n) / (np.pi * n) #making low pass filter
        f = f * (np.cos(w_origin * n)) #moving filter to it's origin to get a band pass filter
        n[l] = 0
        f[l] = wc / np.pi
        self.filter_black = f * window * 2

        if error_db > -21:
            self.filter_best = self.filter_rect
            self.best_name = "Rectangular"
        elif error_db > -25:
            self.filter_best = self.filter_bart
            self.best_name = "Bartlett"
        elif error_db > -44:
            self.filter_best = self.filter_hann
            self.best_name = "Hann"
        elif error_db > -53:
            self.filter_best = self.filter_hamm
            self.best_name = "Hamming"
        else:
            self.filter_best = self.filter_black
            self.best_name = "BlackMan"

    def rectangular(self, delta_w):
        m = int(np.ceil((4 * np.pi) / (2 * delta_w)))
        if m % 2 == 0:
            m = m + 1
        w = signal.boxcar(m)
        return w

    def bartlett(self, delta_w):
        m = int(np.ceil((8 * np.pi) / (2 * delta_w))) + 1
        if m % 2 == 0:
            m = m + 1
        w = signal.bartlett(m)
        return w

    def hann(self, delta_w):
        m = int(np.ceil((8 * np.pi) / (2 * delta_w))) + 1
        if m % 2 == 0:
            m = m + 1
        w = signal.hann(m)
        return w

    def hamming(self, delta_w):
        m = int(np.ceil((8 * np.pi) / (2 * delta_w))) + 1
        if m % 2 == 0:
            m = m + 1
        w = signal.hamming(m)
        return w

    def blackman(self, delta_w):
        m = int(np.ceil((12 * np.pi) / (2 * delta_w))) + 1
        if m % 2 == 0:
            m = m + 1
        w = signal.blackman(m)
        return w

if __name__ == "__main__":
    myfilter = BaseBandFilter(np.pi/6, np.pi/2, 0.1 * np.pi, 0.1)
    print(len(myfilter.filter_best))
    print(myfilter.best_name)
    ffts = np.fft.fft(myfilter.filter_best)
    ffts = np.abs(ffts)
    n = np.arange(len(ffts))
    n = n * 2 * np.pi / len(ffts)
    fig, ax = plt.subplots(1, 1)
    ax.plot(n, ffts)
    plt.show()