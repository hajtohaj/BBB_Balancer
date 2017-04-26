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
            ch = sys.stdin.read_fifo(1)
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

m0 = Motor(0)

speed_step = 10

getch = _Getch()
key_map = {65: 'up', 66: 'down', 67: 'right', 68: 'left', }
c = 'a'

import time
while c != 'q' and c != 'Q':
    c = getch()
    if ord(c) == 27:
        c = getch()
        if ord(c) == 91:
            c = getch()
            if ord(c) in key_map.keys():
                print(key_map[ord(c)])
                if key_map[ord(c)] == 'up':
                    m0.set_voltage(speed_step)
                elif key_map[ord(c)] == 'down':
                    m0.set_voltage(- speed_step)
                if key_map[ord(c)] == 'right':
                    print("{0}".format(m0.get_radians()))
                elif key_map[ord(c)] == 'left':
                    print("{0}".format(m0.get_velocity()))
    elif ord(c) == 32:
        m0.set_velocity(0)
        print("{0}".format(m0.get_velocity()))
    else:
       print(ord(c))
    m0.set_encoder_zero()
    m1.set_encoder_zero()
    time.sleep(0.2)
    enc = m0.get_position()
    m0_enc = m0.get_position()
    m1_enc = m1.get_position()
    print("left: {0}/{1}, right: {2}/{3}".format(m0_enc, m0.get_velocity(), m1_enc, m1.get_velocity()))

    if m0_enc > m1_enc:
        m1.change_rotation(1)
    if m0_enc < m1_enc:
        m1.change_rotation(-1)

m0.close()
m1.close()

