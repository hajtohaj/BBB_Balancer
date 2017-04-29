#!/usr/bin/python3
from motor import Motor
from pid_cotroller import PID
import time


if __name__ == "__main__":

    voltage_level = 20

    given_speed = 6
    step_size = 0.5

    m0 = Motor(0)
    pid = PID(5.0, 10.0, 0.0, 0.1)

    t0 = time.time()
    r0 = m0.get_radians()

    try:
        while 1:
            t1 = time.time()
            r1 = m0.get_radians()

            dt = (t1-t0) % step_size
            dr = r1-r0
            v = dr / dt
            e = given_speed - v
            u = pid.step(e, dt)

            print(e, u)
            m0.set_voltage(u)
            r0 = m0.get_radians()
            t0 = time.time()

            time.sleep(step_size - dt)

    except KeyboardInterrupt:
        m0.close()