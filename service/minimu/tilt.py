from minimu import Minimu
from time import sleep
import numpy as np


if __name__ == "__main__":
    buss_id = 2
    fifo_address = 0x6b

    mm = Minimu(buss_id, fifo_address)
    mm.enable(416)

    av_length = 10

    try:
        while 1:
            acc_data = mm.read_fifo()[-av_length:, -3:]
            acc_data_av = np.average(acc_data, 0)
            print(np.arctan2(acc_data_av[0], acc_data_av[2]), np.arctan2(acc_data_av[1], acc_data_av[2]))
            sleep(0.02)

    except KeyboardInterrupt:
        mm.disable()
