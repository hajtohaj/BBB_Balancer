from minimu import Minimu
from time import sleep
import numpy as np
import sys


if __name__ == "__main__":
    buss_id = 2
    fifo_address = 0x6b

    mm = Minimu(buss_id, fifo_address)
    mm.enable()

    import os
    file_name = '../data/data.txt'
    try:
        os.remove(file_name)
    except OSError:
        pass

    f_handle = open(file_name, 'ab')
    try:
        while 1:

            with open(file_name, 'ab') as f_handle:
                np.savetxt(f_handle, mm.read(), fmt='%d', delimiter=' ')
            sleep(0.07)

    except KeyboardInterrupt:
        mm.disable()
