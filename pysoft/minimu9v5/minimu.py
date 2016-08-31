from pysoft.minimu9v5.gyro import Gyro
from pysoft.minimu9v5.fifo import Fifo
import time

buss_id = 2
address = 0x6b

g = Gyro(buss_id, address)
g.set_full_scale_selection(245)
g.enable_axes('XYZ')
g.set_odr_hz(26)
g.set_hp_filter_hz(16.32)
g.enable_hp_filter()
g.reset_hp_filter()

f = Fifo(buss_id, address)
f.set_gyro_decimation_factor(1)
f.set_odr_hz(26)
f.set_mode('Continuous')

try:
    while 1:
        print(f.get_data())
        time.sleep(1)
except KeyboardInterrupt:
    f.set_mode('Bypass')
    f.set_gyro_decimation_factor(0)
    f.set_odr_hz(0)