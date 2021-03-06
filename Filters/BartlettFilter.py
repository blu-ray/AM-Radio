from numpy import ndarray
import numpy as np
from scipy import signal

from .BaseFilter import BaseFilter

class BartlettFilter(BaseFilter):
    """
    Representing a Bartlet filter. For more information, see the documents of the `BaseFilter`.
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
        m: int = int(np.ceil((8 * np.pi) / (2 * self.delta_w))) + 1
        return m if m % 2 else m + 1

    @property
    def window(self) -> ndarray:
        return signal.bartlett(self.m)
