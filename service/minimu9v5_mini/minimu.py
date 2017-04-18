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

    def enable(self, odr=104):
        self.gyro.enable(odr)
        self.acc.enable(odr)
        self.fifo.enable(odr)


    def disable(self):
        self.gyro.disable()
        self.acc.disable()
        self.fifo.disable()

    def read(self):
        data = np.array(self.fifo.get_data(), dtype=np.int)
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
