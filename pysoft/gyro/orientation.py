from minimu import Minimu
from time import sleep
import numpy as np


if __name__ == "__main__":
    buss_id = 2
    fifo_address = 0x6b

    mm = Minimu(buss_id, fifo_address)
    mm.enable()

    try:
        while 1:
            print(mm.read())
            sleep(1)

    except KeyboardInterrupt:
        mm.disable()