from abc import ABC, abstractmethod
from numpy import ndarray
import numpy as np


class BaseFilter(ABC):
    """
    An abstract class that should be implemented by all filters.
    You should implement `gain` and `m` properties and put the *window* function in the `window` method.
    We made the attributes of the class property functions. Because it's the only way for creating an abstract attribute in the python until version 3.7.
    This class is a filter in the time domain.
    """

    @property
    @abstractmethod
    def m(self) -> int:
        """
        Getter for the *M* value of the filter. M is always an odd number.
        :return:
        """
        return NotImplemented

    @property
    def time(self) -> ndarray:
        """
        This array will compute every time you call this property. So if you want to use the result multiple times
        or you want to modify it, you should first create a copy of the result of this property, then work with that
        copy.
        :return: time spectrum that the signal should apply to it.
        """
        length: int = self.m // 2
        time_array: ndarray = np.arange(-length, length + 1, 1)
        time_array[length] = 0
        return time_array

    @property
    @abstractmethod
    def window(self) -> ndarray:
        """
        Should return window function of the signal in the time domain.
        :return:
        """
        return NotImplemented

    @property
    def cutoff_frequency(self) -> float:
        """
        The desired frequency if radian.
        :return:
        """
        return (self.start_frequency - self.end_frequency) / 2

    @property
    @abstractmethod
    def start_frequency(self) -> float:
        """
        start of the pass band in radian
        :return:
        """
        return NotImplemented

    @property
    @abstractmethod
    def end_frequency(self) -> float:
        """
        End of the pass band in the radian
        :return:
        """
        return NotImplemented

    @property
    def ideal_filter(self) -> ndarray:
        """
        Ideal low-pass filter. the hd in the formula of the Filter function.
        :return:
        """
        time: ndarray = self.time[::]
        time[self.m // 2] = 1
        w_origin: float = (self.start_frequency + self.end_frequency) / 2
        f = np.sin(self.cutoff_frequency * time) / (np.pi * time)
        f[self.m // 2] = self.cutoff_frequency / np.pi
        time[self.m // 2] = 0
        return f * (np.cos(w_origin * time))

    @property
    def h(self) -> ndarray:
        """
        The filter function. It's the result of the multiplying of the ideal_filter and the window property.
        Multiplying by 2 is for normalizing the gain.
        :return:
        """
        return self.ideal_filter * self.window * 2

    def filter(self, signal: ndarray) -> ndarray:
        """
        Applying filter on the input signal and returns the result in the time spectrum.
        Filtering in the time domain is convolving the filter function to the signal.
        :param signal: input signal
        :return: result of multiplication of filter and the signal
        """
        return np.convolve(self.h, signal)