from typing import Union, List
#from numpy import ndarray, array
import numpy as np
from scipy.fftpack import fft
from matplotlib import pyplot as plt

raw_signal_type = Union[np.ndarray, List[int]]


class Signal:
    """
    This class represents a signal. You can access signal values in the time domain using `value` attribute.
    """
    def __init__(self, signal_values: raw_signal_type, sampling_rate: int):
        self.value: np.ndarray = np.array(signal_values)
        self.sampling_rate: int = sampling_rate

    @staticmethod
    def generate_from_file(file_path: str, sampling_rate: int):
        """
        Generates a instance of the `Signal` class from a text file.
        In the text file, each value should be in a separate line.
        :param file_path: Absolute or relative path to the data file.
        :param sampling_rate: The sampling rate of the signal.
        :return: an instance of the Signal.
        """
        with open(file_path, "r") as file:
            raw_signal = [int(x) for x in file.readlines()]
        return Signal(np.array(raw_signal), sampling_rate)

    def get_ft(self) -> np.ndarray:
        """
        :return: Fourier Transform of the signal as a numpy array.
        """
        return fft(self.value)

    def plot_signal_time_domain(self) -> None:
        """
        By calling this method, a plot of the signal in the time domain will draw.
        :return:
        """
        fig, ax = plt.subplots(1, 1)
        ax.plot(np.arange(len(self.value)), self.value)
        plt.show()

    def plot_signal_frequency_domain(self) -> None:
        """
        By calling this method, a plot of the signal in the frequency domain will draw.
        :return:
        """
        fig, ax = plt.subplots(1, 1)
        ax.plot(np.arange(len(self.value)), self.get_ft())
        plt.show()
