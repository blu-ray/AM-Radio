from .BartlettFilter import BartlettFilter, BaseFilter
from .BlackmanFilter import BlackmanFilter
from .HammingFilter import HammingFilter
from .HannFilter import HannFilter
from .RectangularFilter import RectangularFilter
import numpy as np

def best_filter(w_start: float, w_end: float, delta_w: float, error: float) -> BaseFilter:
    """
    This function calculates the `20 * log error` firstly. Then looks for the first signal with the values of
    filters. First filter with lesser value will choose and an instance of that filter will create and return.

        |Chosen Filter| < 20 * log error |
        | ------------- | ------------------ |
        | Rectangula    | -21                |
        | Bartlett      | -25                |
        | Hann          | -44                |
        | Hamming       | -53                |
        | Blackman      | -74                |

    :param w_start: in radian
    :param w_end: in radian
    :param delta_w:
    :param error:
    :return:
    """
    error_db = 20 * np.log10(error)
    if error_db > -21:
        return RectangularFilter(delta_w, w_start, w_end)
    elif error_db > -25:
        return BartlettFilter(delta_w, w_start, w_end)
    elif error_db > -44:
        return HannFilter(delta_w, w_start, w_end)
    elif error_db > -53:
        return HammingFilter(delta_w, w_start, w_end)
    else:
        return BlackmanFilter(delta_w, w_start, w_end)
