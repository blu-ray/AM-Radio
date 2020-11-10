from Filters.BaseFilter import BaseFilter
from Radio.Signal import Signal
import numpy as np
from Filters.filter import best_filter


class Radio:
    """
    This class represents an AM radio. You can call demodulate method for getting human audible signal.
    This class has 3 class attributes:
    1- hertz_to_radian: the factor you should multiply to the hertz values for converting them from Hertz to the Radian. This value is dependent to the signal
                        sampling rate and should replace with correct value if sampling rate is not 480 KHz.
    2- delta_w: The pass width. Decreasing this value will increase the number of needed sentences and increases delay.
    3- voice_gain: The final voice will multiply to this number for increasing the amplitude of the voice.
    """
    hertz_to_radian: float = np.pi / 240
    delta_w: float = 0.1 * np.pi
    voice_gain: int = 1

    def __init__(self, signal: Signal, error: float):
        """
        :param signal The signal that has been get from antenna
        :param error Maximum acceptable error rate
        """
        self.signal: Signal = signal
        self.error: float = error

    def get_channel_filter(self, start_freq: float, end_freq: float) -> BaseFilter:
        """
        This method only returns the result of the `best_filter` function. Passes `delta_w` attribute of the
        Radio as `delta_w` parameter of that function.
        :param start_freq: in radian
        :param end_freq: in radian
        :return:
        """
        return best_filter(start_freq, end_freq, Radio.delta_w, self.error)

    def get_low_pass_filter(self) -> BaseFilter:
        """
        This method only returns the result of the `best_filter` function. Passes `delta_w` attribute of the
        Radio as `delta_w` parameter of that function. Also passes 0 for `w_start` and `20 * Radio.hertz_to_radian` as `w_end`.
        :return:
        """
        return best_filter(0, 20 * Radio.hertz_to_radian, Radio.delta_w, self.error)

    def get_shifted_signal(self, channel_filter: BaseFilter, desired_frequency: float) -> np.ndarray:
        """
        This method first filters the input signal by `channel_filter` and extracts the desired channel from the input.
        Then by multiplying That signal to the Carrier signal, shifts that.
        :param channel_filter: Probably the result of the `get_channel_filter` method.
        :param desired_frequency: The frequency of the channel in radian.
        :return: shifted signal as a numpy array.
        """
        channel_sig: np.ndarray = channel_filter.filter(self.signal.value)
        n = np.arange(len(channel_sig))
        return channel_sig * (np.cos(desired_frequency * Radio.hertz_to_radian * n))

    def demodulate(self, desired_frequency: float) -> Signal:
        """
        Demodulates the signal that has been get from the antenna and returns human audible signal from it.
        :param desired_frequency: frequency of the desired station in Hertz.
        :return: Voice signal prepared for writing as a wav file.
        """
        start_freq: float = (desired_frequency - 24) * Radio.hertz_to_radian
        end_freq: float = (desired_frequency + 24) * Radio.hertz_to_radian
        channel_filter: BaseFilter = self.get_channel_filter(start_freq, end_freq)
        low_pass_filter: BaseFilter = self.get_low_pass_filter()
        voice_sig: np.ndarray = low_pass_filter.filter(self.get_shifted_signal(channel_filter, desired_frequency))
        return Signal(np.array([Radio.voice_gain * voice_sig[10*x] for x in range(0, 480000)]), 44100)
