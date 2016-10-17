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


from pwm import Pwm

pwm0 = Pwm(0)
pwm0_step = 100000
pwm1 = Pwm(1)
pwm1_step = 100000

from gpio import Gpio
gpio36 = Gpio(36)
gpio36.set_direction_out()
gpio36.set_value_low()
gpio62 = Gpio(62)
gpio62.set_direction_out()
gpio62.set_value_low()

gpio26 = Gpio(26)
gpio26.set_direction_out()
gpio26.set_value_low()
gpio47 = Gpio(47)
gpio47.set_direction_out()
gpio47.set_value_low()


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
                    pwm0.set_duty_cycle(str(int(pwm0.get_duty_cycle()) + pwm0_step))
                    pwm1.set_duty_cycle(str(int(pwm1.get_duty_cycle()) + pwm1_step))
                elif key_map[ord(c)] == 'down':
                    pwm0.set_duty_cycle(str(int(pwm0.get_duty_cycle()) - pwm0_step))
                    pwm1.set_duty_cycle(str(int(pwm1.get_duty_cycle()) - pwm1_step))

                if key_map[ord(c)] == 'right':
                    pwm0.set_duty_cycle(str(int(pwm0.get_duty_cycle()) + pwm0_step/2))
                    pwm1.set_duty_cycle(str(int(pwm1.get_duty_cycle()) - pwm1_step/2))
                elif key_map[ord(c)] == 'left':
                    pwm0.set_duty_cycle(str(int(pwm0.get_duty_cycle()) - pwm0_step/2))
                    pwm1.set_duty_cycle(str(int(pwm1.get_duty_cycle()) + pwm1_step/2))
    elif ord(c) == 32:
        pwm0.set_duty_cycle(0)
        pwm1.set_duty_cycle(0)
        gpio36.set_value_low()
        gpio62.set_value_low()
        gpio26.set_value_low()
        gpio47.set_value_low()
    else:
       print(ord(c))

