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
m1 = Motor(1)
speed_step = 6

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
                    m0.change_velocity(- speed_step)
                    m1.change_velocity(speed_step)
                    print("left: {0}, right: {1}".format(m0.get_velocity(), m1.get_velocity()))
                elif key_map[ord(c)] == 'down':
                    m0.change_velocity(speed_step)
                    m1.change_velocity(- speed_step)
                    print("left: {0}, right: {1}".format(m0.get_velocity(), m1.get_velocity()))
                if key_map[ord(c)] == 'right':
                    m0_vel = m0.get_velocity()
                    m0.change_velocity(sign(m0_vel) * speed_step)
                    print("left: {0}, right: {1}".format(m0.get_velocity(), m1.get_velocity()))
                elif key_map[ord(c)] == 'left':
                    m0_vel = m0.get_velocity()
                    m0.change_velocity(-sign(m0_vel) * speed_step)
                    print("left: {0}, right: {1}".format(m0.get_velocity(), m1.get_velocity()))
    elif ord(c) == 32:
        m0.set_velocity(0)
        m1.set_velocity(0)
        print("left: {0}, right: {1}".format(m0.get_velocity(), m1.get_velocity()))
    else:
       print(ord(c))

m0.close()
m1.close()

