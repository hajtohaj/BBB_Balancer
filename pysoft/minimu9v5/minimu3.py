from gyro import Gyro
from acc import Acc
from fifo import Fifo
import time
import math


class Minimu():
    MAX_POSITIVE_16 = 32767.0
    MIN_NEGATIVE_16 = 32768.0

    def __init__(self, buss_id, address):
        self.gyro = Gyro(buss_id, address)
        self.acc = Acc(buss_id, address)
        self.fifo = Fifo(buss_id, address)
        self.gyro_full_scale = 245
        self.gyro_odr_hz = 104
        self.gyro_axes = 'XYZ'
        self.gyro_angles = dict(X=0, Y=0, Z=0)
        self.gyro_positive_factor = self.gyro_full_scale / self.MAX_POSITIVE_16
        self.gyro_negative_factor = self.gyro_full_scale / self.MIN_NEGATIVE_16
        self.acc_full_scale = 2
        self.acc_odr_hz = self.gyro_odr_hz
        self.acc_axes = 'XYZ'
        self.acc_positive_factor = self.acc_full_scale / self.MAX_POSITIVE_16
        self.acc_negative_factor = self.acc_full_scale / self.MIN_NEGATIVE_16

    def setup_gyro(self):
        self.gyro.set_full_scale_selection(self.gyro_full_scale)
        self.gyro.enable_axes(self.gyro_axes)
        self.gyro.set_odr_hz(self.gyro_odr_hz)

    def disable_gyro(self):
        self.gyro.set_odr_hz(0)
        self.gyro.disable_axes(self.gyro_axes)

    def setup_acc(self):
        self.acc.set_full_scale_selection(self.acc_full_scale)
        self.acc.enable_axes(self.acc_axes)
        self.acc.set_odr_hz(self.acc_odr_hz)

    def disable_acc(self):
        self.acc.set_odr_hz(0)
        self.acc.disable_axes(self.acc_axes)

    def setup_fifo(self):
        self.fifo.set_gyro_decimation_factor(1)
        self.fifo.set_acc_decimation_factor(1)
        self.fifo.set_odr_hz(self.gyro_odr_hz)
        self.fifo.set_mode('Continuous')

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
        fifo_pattern_size = 6
        data = self.fifo.get_data(fifo_pattern_size)
        radian_factor = 3.14159265359 / 180.0
        gyro_pitch = [d * self.gyro_positive_factor * radian_factor if d >= 0 else d * self.gyro_negative_factor * radian_factor for d in data[0]]
        acc_y = [d * self.acc_positive_factor if d >= 0 else d * self.acc_negative_factor for d in data[4]]
        acc_z = [d * self.acc_positive_factor if d >= 0 else d * self.acc_negative_factor for d in data[5]]
        acc_pitch = [math.atan2(y, z) for y, z in zip(acc_y, acc_z)]
        return [(x,y) for x,y in zip(gyro_pitch, acc_pitch)]


if __name__ == "__main__":
    buss_id = 2
    fifo_address = 0x6b

    mm = Minimu(buss_id, fifo_address)
    mm.setup_gyro()
    mm.setup_acc()
    mm.setup_fifo()

    try:
        while 1:
            print(mm.read())
            time.sleep(2)
    except KeyboardInterrupt:
        mm.disable_fifo()
        mm.disable_gyro()
        mm.disable_acc()
