#!/usr/bin/python3
from motor import Motor
from pid_cotroller import PID
import time


if __name__ == "__main__":

    speed = 6.0
    step_size = 0.01

    m0 = Motor(0)
    pid = PID(1.0, 10.0, 0.0, 0.1)

    t0 = time.time()
    r0 = m0.get_radians()

    try:
        while 1:
            t1 = time.time()
            r1 = m0.get_radians()

            dt = t1 - t0
            dr = r1 - r0
            v = dr / dt
            e = speed - v
            u = pid.step(e, dt)

            print("{0:9.6f}, {1:9.6f}, {2:9.6f}, {3:9.6f}, {4:9.6f}".format(dt, dr, v, e, u))
            m0.set_voltage(-u)
            r0 = m0.get_radians()
            t0 = time.time()

            time.sleep(step_size)

    except KeyboardInterrupt:
        m0.close()