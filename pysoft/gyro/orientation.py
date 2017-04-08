from minimu import Minimu
from time import sleep
import numpy as np
import sys


if __name__ == "__main__":
    buss_id = 2
    fifo_address = 0x6b

    mm = Minimu(buss_id, fifo_address)
    mm.enable()

    try:
        while 1:
            np.savetxt(sys.stdout.buffer, mm.read(), fmt='%i', delimiter='; ')
            sleep(1)

    except KeyboardInterrupt:
        mm.disable()