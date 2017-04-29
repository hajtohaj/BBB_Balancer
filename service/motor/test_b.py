#!/usr/bin/python3
from motor import Motor
from pid_controller import PID
import time

if __name__ == "__main__":

    voltage_level = 15
    delta_t = 0.1

    m0 = Motor(0)
    pid = PID(20.0, 0.5, 0.0, 0.1)

    r0 = m0.get_radians()

    try:
        while 1:
            t0 = time.time()

            r1 = m0.get_radians()
            print(r0)

            m0.set_voltage(voltage_level)

            t1 = time.time()
            time.sleep(delta_t - (t1 - t0) % delta_t)
            print(time.time())
            r1 = m0.get_radians()
    except KeyboardInterrupt:
        m0.close()