from gyro import Gyro
from acc import Acc
from fifo import Fifo
import time
import numpy as np


class Minimu:
    MAX_POSITIVE_16 = 32767.0
    MIN_NEGATIVE_16 = 32768.0

    # STATIC_OFFSET = np.array([520, -465, -539, -501, -206, 244])

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

        # self.offset = self.STATIC_OFFSET
        # self.variance = None
        # self.mean = None

    # def calculate_noise(self, gyro_data):
    #     self.mean = np.nanmean(gyro_data, axis=0)
    #     self.variance = np.nanvar(gyro_data, axis=0)
    #     return np.vstack((self.mean, self.variance))

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
        time.sleep(0.2) #needed for gyro

    def disable_fifo(self):
        self.fifo.set_mode('Bypass')
        self.fifo.set_gyro_decimation_factor(0)
        self.fifo.set_acc_decimation_factor(0)
        self.fifo.set_odr_hz(0)
    #
    # def to_angle(self, sample_sum):
    #     if sample_sum >= 0:
    #         return sample_sum * self.gyro_positive_factor
    #     else:
    #         return sample_sum * self.gyro_negative_factor

    def read(self):
        data = np.array(self.fifo.get_data(), dtype=np.float)
        data[:, 0:6] -= self.offset[0:6]
        return data


if __name__ == "__main__":
    buss_id = 2
    fifo_address = 0x6b

    np.set_printoptions(precision=3)

    mm = Minimu(buss_id, fifo_address)
    mm.setup_gyro()
    mm.setup_acc()
    mm.setup_fifo()

    try:
        while 1:
            dd = mm.read()
            print(dd)
            # mm.calculate_noise(dd)
            # print(mm.mean)
            # print(mm.variance)
            # # np.savetxt(f,mm.mean.reshape(1,6), fmt='%8.2f %8.2f %8.2f %8.2f %8.2f %8.2f')
            print()
            time.sleep(0.5)
    except KeyboardInterrupt:
        # print(mm.mean)
        # print(mm.variance)
        mm.disable_fifo()
        mm.disable_gyro()
        mm.disable_acc()
