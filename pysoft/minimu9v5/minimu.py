from gyro import Gyro
from fifo import Fifo
import time


class Minimu():

    ODR_HZ = 52
    GYRO_FULL_SCALE = 245
    GYRO_HP_BANDWIDTH = 0.0324
    GYRO_OFFSET = 0
    GYRO_POSITIVE_FACTOR = GYRO_FULL_SCALE / 32767.0 / ODR_HZ
    GYRO_NEGATIVE_FACTOR = GYRO_FULL_SCALE / 32768.0 / ODR_HZ

    def __init__(self, buss_id, address):
        self.gyro = Gyro(buss_id, address)
        self.fifo = Fifo(buss_id, address)
        self.angles = dict(X=0, Y=0, Z=0)

    def setup_gyro(self):
        self.gyro.set_full_scale_selection(self.GYRO_FULL_SCALE)
        self.gyro.enable_axes('XYZ')
        self.gyro.set_odr_hz(self.ODR_HZ)
        self.gyro.set_hp_filter_hz(self.GYRO_HP_BANDWIDTH)
        self.gyro.enable_hp_filter()
        self.gyro.reset_hp_filter()

    def disable_gyro(self):
        self.gyro.disable_hp_filter()
        self.gyro.set_hp_filter_hz(0.0081)
        self.gyro.set_odr_hz(0)
        self.gyro.disable_axes('XYZ')

    def setup_fifo(self):
        self.fifo.set_gyro_decimation_factor(1)
        self.fifo.set_odr_hz(self.ODR_HZ)
        self.fifo.set_mode('Continuous')
        print(self.fifo.get_data())  # discard first sample
        print(self.fifo.get_data())  # discard second sample
        time.sleep(0.25)

    def disable_fifo(self):
        self.fifo.set_mode('Bypass')
        self.fifo.set_gyro_decimation_factor(0)
        self.fifo.set_odr_hz(0)

    def to_angle(self, sample_sum, sample_count):
        if sample_sum >= 0:
            return sample_sum * self.GYRO_POSITIVE_FACTOR + sample_count * self.GYRO_OFFSET
        else:
            return sample_sum * self.GYRO_NEGATIVE_FACTOR + sample_count * self.GYRO_OFFSET

    def read_gyro(self):
        data = self.fifo.get_data()
        print("D", data)
        if data:
            x = self.to_angle(data[0][0], data[0][1])
            y = self.to_angle(data[1][0], data[1][1])
            z = self.to_angle(data[2][0], data[2][1])
            self.angles['X'] += x
            self.angles['Y'] += y
            self.angles['Z'] += z
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
            print("Radians: X: {0:.12f},  Y: {1:.12f}, Z:  {2:.12f}".format(self.__degree_to_radian(self.angles['X']),
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
            print("Last reading: {0}".format(mm.read_gyro()))
            mm.print_angles_degrees()
            mm.print_angles_radians()
            time.sleep(1)
    except KeyboardInterrupt:
        pass
        #mm.disable_fifo()
        #mm.disable_gyro()
