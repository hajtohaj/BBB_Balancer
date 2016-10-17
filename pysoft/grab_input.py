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


from pysoft.motor.pwm import Pwm

pwm0 = Pwm(0)
pwm0_step = 100000
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
                    pwm0.set_duty_cycle(pwm0.get_duty_cycle() + pwm0_step)
                elif key_map[ord(c)] == 'down':
                    pwm0.set_duty_cycle(pwm0.get_duty_cycle() - pwm0_step)
    else:
       print(ord(c))

