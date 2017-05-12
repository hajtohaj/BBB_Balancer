from motor import Motor
import smbus
import time

class Rcradio:

    def __init__(self, bus_id, radio_id):
        self.bus_id = bus_id
        self.radio_id = radio_id
        self.bus = smbus.SMBus(self.bus_id)

    def red_chanel(self, ch_id):
        w = self.bus.read_word_data(self.radio_id, ch_id)
        return w

if __name__ == "__main__":

    m0 = Motor(0)
    rc = Rcradio(2, 0x10)
    offset = 698

    try:
        while 1:
            speed = offset - rc.red_chanel(0)
            if abs(speed) < 3:
                speed = 0
            print(speed)
            m0.set_voltage(speed)
            time.sleep(0.1)

    except KeyboardInterrupt:
        m0.close()
        pass
