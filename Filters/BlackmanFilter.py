from numpy import ndarray
import numpy as np
from .BaseFilter import BaseFilter
from scipy import signal


class BlackmanFilter(BaseFilter):
    """
    Representing the Blackman filter in the time domain. For more information, see the documents of the `BaseFilter`.
    """

    def __init__(self, delta_w: float, start_freq: float, end_freq: float):
        self.delta_w: float = delta_w
        self._s_fre: float = start_freq
        self._e_fre: float = end_freq

    @property
    def start_frequency(self) -> float:
        return self._s_fre

    @property
    def end_frequency(self) -> float:
        return self._e_fre

    @property
    def m(self) -> int:
        m: int = int(np.ceil((12 * np.pi) / (2 * self.delta_w))) + 1
        return m if m % 2 else m + 1

    @property
    def window(self) -> ndarray:
        return signal.blackman(self.m)
