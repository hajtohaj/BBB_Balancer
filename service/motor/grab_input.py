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

m0 = Motor(0)

voltage_step = 10
voltage = 0

getch = _Getch()
key_map = {65: 'up', 66: 'down', 67: 'right', 68: 'left', }
c = 'a'
while c != 'q' and c != 'Q':
    c = getch()
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
        m0.set_velocity(0)
        print("{0}".format(m0.get_velocity()))
    else:
        print(ord(c))
    if voltage > 100:
        volate = 100
    if voltage < -100:
        voltage = -100
    m0.set_voltage(voltage)

m0.set_encoder(0)
m0.close()
