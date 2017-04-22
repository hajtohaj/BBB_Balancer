from minimu import Minimu
from time import sleep
import numpy as np


if __name__ == "__main__":
    buss_id = 2
    fifo_address = 0x6b

    mm = Minimu(buss_id, fifo_address)
    mm.enable(104)

    try:
        while 1:
            n = mm.read_fifo()
            print(np.average(n[-10:, -3:], 0))
            sleep(0.1)

    except KeyboardInterrupt:
        mm.disable()
