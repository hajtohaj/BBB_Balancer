class _Getch:
    """Gets a single character from standard input.  Does not echo to the
screen."""
    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()

    def __call__(self): return self.impl()


class _GetchUnix:
    def __init__(self):
        import tty, sys

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


class _GetchWindows:
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        return msvcrt.getch()

def sign(a):
    return (a >= 0) - (a < 0)

from motor import Motor
import time

m0 = Motor(0)

voltage_step = 10
voltage = 0

getch = _Getch()
key_map = {65: 'up', 66: 'down', 67: 'right', 68: 'left', }
c = 'a'
while c != 'q' and c != 'Q':
    t0 = time.time()
    r0 = m0.get_radians()
    c = getch()
    t1 = time.time()
    r1 = m0.get_radians()
    print("{0}, {1}".format(voltage, (r1 - r0)/(t1 - t0)))
    if ord(c) == 27:
        c = getch()
        if ord(c) == 91:
            c = getch()
            if ord(c) in key_map.keys():
                print(key_map[ord(c)])
                if key_map[ord(c)] == 'up':
                    voltage += voltage_step
                elif key_map[ord(c)] == 'down':
                    voltage -= voltage_step
    elif ord(c) == 32:
        pass
    else:
        print(ord(c))
    if voltage > 100:
        volate = 100
    if voltage < -100:
        voltage = -100
    m0.get_radians()
    m0.set_voltage(voltage)

m0.set_encoder(0)
m0.close()
