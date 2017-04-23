#!/usr/bin/python3
from motor2 import Motor
import time

if __name__ == "__main__":

    voltage_level = -15

    m0 = Motor(0)
    m1 = Motor(1,-1)

    try:
        while 1:
            print(m0.get_radians(), m1.get_radians())
            m0.set_voltage(voltage_level)
            m1.set_voltage(voltage_level)
            time.sleep(0.25)

    except KeyboardInterrupt:
        m0.close()
        m1.close()