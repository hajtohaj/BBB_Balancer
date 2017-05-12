from motor import Motor
import smbus
import time

class Rcradio:

    def __init__(self, bus_id, radio_id):
        self.bus_id = bus_id
        self.radio_id = radio_id
        self.bus = smbus.SMBus(self.bus_id)

    def red_chanel(self, ch_id):
        w = self.bus.read_word_data(self.radio_id, self.ch_id)
        return w

if __name__ == "__main__":

    # m0 = Motor(0)
    rc = Rcradio(2, 0x10)

    try:
        while 1:
            # print(m0.get_radians())
            # m0.set_voltage(voltage_level)
            print(rc.red_chanel(0))
            time.sleep(0.25)

    except KeyboardInterrupt:
        # m0.close()
        pass
