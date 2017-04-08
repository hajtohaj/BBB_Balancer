from gyro import Gyro
from acc import Acc
from fifo import Fifo
from time import sleep
import numpy as np
import sys


class Minimu:

    def __init__(self, buss_id, address):
        self.gyro = Gyro(buss_id, address)
        self.acc = Acc(buss_id, address)
        self.fifo = Fifo(buss_id, address)
        self.gyro_full_scale = 245
        self.gyro_axes = 'XYZ'
        self.acc_full_scale = 2
        self.acc_axes = 'XYZ'
        self.odr_hz = 104

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

    def disable_fifo(self):
        self.fifo.set_mode('Bypass')
        self.fifo.set_gyro_decimation_factor(0)
        self.fifo.set_acc_decimation_factor(0)
        self.fifo.set_odr_hz(0)

    def enable(self):
        self.setup_gyro()
        self.setup_acc()
        self.setup_fifo()

    def disable(self):
        self.disable_fifo()
        self.disable_acc()
        self.disable_gyro()

    def read(self):
        data = np.array(self.fifo.get_data(), dtype=np.int16)
        return data

if __name__ == "__main__":
    buss_id = 2
    fifo_address = 0x6b

    np.set_printoptions(precision=3)

    mm = Minimu(buss_id, fifo_address)
    mm.enable()

    try:
        while 1:
            np.savetxt(sys.stdout.buffer, mm.read(), fmt='%i', delimiter='; ')
            sleep(1)

    except KeyboardInterrupt:
        mm.disable()
