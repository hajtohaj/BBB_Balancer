from minimu import Minimu
from time import sleep
import numpy as np


if __name__ == "__main__":
    buss_id = 2
    fifo_address = 0x6b

    mm = Minimu(buss_id, fifo_address)
    mm.enable(208)

    av_length = 10

    try:
        while 1:
            acc_data = mm.read_fifo()[-av_length:, -3:]
            acc_data_av = np.average(acc_data, 0)
            print(np.arctan2(acc_data_av[2], acc_data_av[1]), np.arctan2(acc_data_av[1], acc_data_av[2]))  # fi = np.arctan2(y, z)
            sleep(0.01)

    except KeyboardInterrupt:
        mm.disable()
