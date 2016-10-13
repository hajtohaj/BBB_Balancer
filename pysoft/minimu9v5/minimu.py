from gyro import Gyro
from acc import Acc
from fifo import Fifo
import time
import numpy as np


class Minimu:
    MAX_POSITIVE_16 = 32767.0
    MIN_NEGATIVE_16 = 32768.0

    def __init__(self, buss_id, address):
        self.gyro = Gyro(buss_id, address)
        self.acc = Acc(buss_id, address)
        self.fifo = Fifo(buss_id, address)
        self.gyro_full_scale = 245
        self.gyro_axes = 'XYZ'
        self.gyro_positive_factor = self.gyro_full_scale / self.MAX_POSITIVE_16
        self.gyro_negative_factor = self.gyro_full_scale / self.MIN_NEGATIVE_16
        self.acc_full_scale = 2
        self.acc_axes = 'XYZ'
        self.acc_positive_factor = self.acc_full_scale / self.MAX_POSITIVE_16
        self.acc_negative_factor = self.acc_full_scale / self.MIN_NEGATIVE_16
        self.odr_hz = 104

        self.variance = np.zeros(9)
        self.mean = np.zeros(9)

    def calculate_noise(self, gyro_data):
        self.mean = np.nanmean(gyro_data, axis=0)
        self.variance = np.nanvar(gyro_data, axis=0)
        return np.vstack((self.mean, self.variance))

    def setup_gyro(self):
        self.gyro.set_full_scale_selection(self.gyro_full_scale)
        self.gyro.enable_axes(self.gyro_axes)
        self.gyro.set_odr_hz(self.odr_hz)

    def disable_gyro(self):
        self.gyro.set_odr_hz(0)
        self.gyro.disable_axes(self.gyro_axes)

    def setup_acc(self):
        self.acc.set_full_scale_selection(self.acc_full_scale)
        self.acc.enable_axes(self.acc_axes)
        self.acc.set_odr_hz(self.odr_hz)

    def disable_acc(self):
        self.acc.set_odr_hz(0)
        self.acc.disable_axes(self.acc_axes)

    def setup_fifo(self):
        self.fifo.set_odr_hz(self.odr_hz)
        self.fifo.set_gyro_decimation_factor(1)
        self.fifo.set_acc_decimation_factor(1)
        self.fifo.set_mode('Continuous')
        time.sleep(1) # gyro needs this (checked experymentaly)
        self.calculate_noise(np.array(mm.read(),dtype=np.float))

    def disable_fifo(self):
        self.fifo.set_mode('Bypass')
        self.fifo.set_gyro_decimation_factor(0)
        self.fifo.set_acc_decimation_factor(0)
        self.fifo.set_odr_hz(0)

    def to_angle(self, sample_sum):
        if sample_sum >= 0:
            return sample_sum * self.gyro_positive_factor
        else:
            return sample_sum * self.gyro_negative_factor

    def read(self):
        data = self.fifo.get_data()
        return data


if __name__ == "__main__":
    buss_id = 2
    fifo_address = 0x6b

    mm = Minimu(buss_id, fifo_address)
    mm.setup_gyro()
    mm.setup_acc()
    mm.setup_fifo()

    try:
        while 1:
            dd = np.array(mm.read())
            noise = mm.calculate_noise(dd)
            print(noise)
            time.sleep(1)
    except KeyboardInterrupt:
        mm.disable_fifo()
        mm.disable_gyro()
        mm.disable_acc()
