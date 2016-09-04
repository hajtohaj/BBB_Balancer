from gyro import Gyro
from fifo import Fifo
import time


class Minimu():
    MAX_POSITIVE_16 = 32767.0
    MIN_NEGATIVE_16 = 32768.0

    def __init__(self, buss_id, address):
        self.gyro = Gyro(buss_id, address)
        self.fifo = Fifo(buss_id, address)
        self.gyro_full_scale = 245
        self.odr_hz = 416
        self.gyro_hp_filter_bdwt = 0.0324
        self.gyro_axes = 'X'
        self.angles = dict(X=0, Y=0, Z=0)
        self.gyro_positive_factor = self.gyro_full_scale / self.MAX_POSITIVE_16 / self.odr_hz
        self.gyro_negative_factor = self.gyro_full_scale / self.MIN_NEGATIVE_16 / self.odr_hz

    def setup_gyro(self):
        self.gyro.set_full_scale_selection(self.gyro_full_scale)
        self.gyro.enable_axes(self.gyro_axes)
        self.gyro.set_odr_hz(self.odr_hz)
        self.gyro.set_hp_filter_hz(self.gyro_hp_filter_bdwt)
        self.gyro.enable_hp_filter()
        self.gyro.reset_hp_filter()

    def disable_gyro(self):
        self.gyro.set_odr_hz(0)
        self.gyro.disable_axes(self.gyro_axes)
        self.gyro.disable_hp_filter()
        self.gyro.set_hp_filter_hz(0.0081)

    def setup_fifo(self):
        self.fifo.set_gyro_decimation_factor(1)
        self.fifo.set_odr_hz(self.odr_hz)
        self.fifo.set_mode('Continuous')
        time.sleep(1)
        print(self.fifo.get_data())  # discard first samples

    def disable_fifo(self):
        self.fifo.set_mode('Bypass')
        self.fifo.set_gyro_decimation_factor(0)
        self.fifo.set_odr_hz(0)

    def to_angle(self, sample_sum):
        if sample_sum >= 0:
            return sample_sum * self.gyro_positive_factor
        else:
            return sample_sum * self.gyro_negative_factor

    def read_gyro(self):
        data = self.fifo.get_data()
        if data:
            x = self.to_angle(data[0][0])
            y = self.to_angle(data[1][0])
            z = self.to_angle(data[2][0])
            self.angles['X'] += round(x, 2)
            self.angles['Y'] += round(y, 2)
            self.angles['Z'] += round(z, 2)
            return {'X': x, 'Y': y, 'Z': z}
        else:
            return dict(X=0, Y=0, Z=0)

    def print_angles_degrees(self):
        print("Degrees: X: {0:.12f},  Y: {1:.12f}, Z:  {2:.12f}".format(self.angles['X'],
                                                                        self.angles['Y'], self.angles['Z']))

    @staticmethod
    def __degree_to_radian(degrees):
        return degrees * 3.14159265/180

    def print_angles_radians(self):
            print("Radians: X: {0:.12f},  Y: {1:.12f}, Z:  {2:.12f}\r".format(self.__degree_to_radian(self.angles['X']),
                                                                self.__degree_to_radian(self.angles['Y']),
                                                                self.__degree_to_radian(self.angles['Z'])))

if __name__ == "__main__":
    buss_id = 2
    fifo_address = 0x6b

    mm = Minimu(buss_id, fifo_address)
    mm.setup_gyro()
    mm.setup_fifo()

    try:
        while 1:
            mm.read_gyro()
            mm.print_angles_degrees()
            time.sleep(1)
    except KeyboardInterrupt:
        mm.disable_fifo()
        mm.disable_gyro()
