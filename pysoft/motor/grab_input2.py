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

from motor2 import Motor

m0 = Motor(0)
m1 = Motor(1, -1)
speed_step = 10

getch = _Getch()
key_map = {65:'up', 66:'down', 67:'right', 68:'left', }
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
                    if m0.get_voltage_level() > m1.get_voltage_level():
                        m1.set_voltage_level(m0.get_voltage_level())
                        m1.set_direction(m0.get_direction())
                    elif m0.get_voltage_level() < m1.get_voltage_level():
                        m0.set_voltage_level(m1.get_voltage_level())
                        m0.set_direction(m1.get_direction())
                    else:
                        if (m0.get_voltage_level() + speed_step) > 0 and (m0.get_direction() < 0):
                            m0.reverse_direction()
                        if (m1.get_voltage_level() + speed_step) > 0 and (m1.get_direction() < 0):
                            m1.reverse_direction()
                        if m0.is_stopped():
                            m0.set_direction_cw()
                            m0.set_direction_ccw()
                        m0.set_voltage_level(m0.get_voltage_level() + speed_step)
                        m1.set_voltage_level(m1.get_voltage_level() + speed_step)
                    print("left: {0}, right: {1}".format(m0.get_voltage_level(), m1.get_voltage_level()))
                elif key_map[ord(c)] == 'down':
                    if m0.get_voltage_level() > m1.get_voltage_level():
                        m1.set_voltage_level(m0.get_voltage_level())
                        m1.set_direction(m0.get_direction())
                    elif m0.get_voltage_level() < m1.get_voltage_level():
                        m0.set_voltage_level(m1.get_voltage_level())
                        m0.set_direction(m1.get_direction())
                    else:
                        if (m0.get_voltage_level() - speed_step) < 0 and (m0.get_direction() > 0):
                            m0.reverse_direction()
                        if (m1.get_voltage_level() - speed_step < 0) and (m1.get_direction() > 0):
                            m1.reverse_direction()
                        if m0.is_stopped():
                            m0.set_direction_cw()
                            m0.set_direction_ccw()
                        m0.set_voltage_level(m0.get_voltage_level() - speed_step)
                        m1.set_voltage_level(m1.get_voltage_level() - speed_step)
                    print("left: {0}, right: {1}".format(m0.get_voltage_level(), m1.get_voltage_level()))
                if key_map[ord(c)] == 'right':
                    if (m0.get_voltage_level() - speed_step) < 0 and (m0.get_direction() > 0):
                        m0.reverse_direction()
                    if m0.is_stopped():
                        m0.set_direction_ccw()
                    m0.set_voltage_level(m0.get_voltage_level() - speed_step)
                    print("left: {0}, right: {1}".format(m0.get_voltage_level(), m1.get_voltage_level()))
                elif key_map[ord(c)] == 'left':
                    if (m1.get_voltage_level() - speed_step < 0) and (m1.get_direction() > 0):
                        m1.reverse_direction()
                    if m1.is_stopped():
                        m1.set_direction_ccw()
                    m1.set_voltage_level(m1.get_voltage_level() - speed_step)
                    print("left: {0}, right: {1}".format(m0.get_voltage_level(), m1.get_voltage_level()))
    elif ord(c) == 32:
        m0.stop()
        m0.set_voltage_level(m0.get_voltage_level() + speed_step)
        m1.stop()
        m1.set_voltage_level(m1.get_voltage_level() + speed_step)
        print("left: {0}, right: {1}".format(m0.get_voltage_level(), m1.get_voltage_level()))
    else:
       print(ord(c))

m0.close()
m1.close()

