from gpio import Gpio
from pwm import Pwm
from eqep import Eqep


class Motor:

    MAX_SPEED = 100
    MIN_SPEED = 0

    __SPEED_FACTOR = 10000

    DIRECTION = {'01': 'cw', '10': 'ccw', '00': 'stop', '11': 'stop_high'}

    def __init__(self, motor_id):
        self.motor_id = motor_id

        if self.motor_id:
            self.pwm = Pwm(1)
            self.pin_a = Gpio(26)
            self.pin_b = Gpio(47)
        else:
            self.pwm = Pwm(0)
            self.pin_a = Gpio(36)
            self.pin_b = Gpio(62)

        self.pwm.export()
        self.pwm.set_period(self.MAX_SPEED * self.__SPEED_FACTOR)
        self.pwm.set_duty_cycle(0)
        self.pwm.enable()

        self.pin_a.export()
        self.pin_a.set_direction_out()
        self.pin_a.set_low()

        self.pin_b.export()
        self.pin_b.set_direction_out()
        self.pin_b.set_low()

    def set_speed(self, speed):
        if speed > self.MAX_SPEED:
            speed = self.MAX_SPEED
        elif speed < 0:
            speed = self.MIN_SPEED
        speed *= self.__SPEED_FACTOR
        print(speed)
        self.pwm.set_duty_cycle(speed)

    def get_speed(self):
        return self.pwm.get_duty_cycle()/self.__SPEED_FACTOR

    def set_direction(self, direction):
        if direction == 'cw':
            self.pin_a.set_low()
            self.pin_b.set_high()
        elif direction == 'ccw':
            self.pin_a.set_high()
            self.pin_b.set_low()
        elif direction == 'stop':
            m0.set_speed(0)
            self.pin_a.set_low()
            self.pin_b.set_low()
        elif direction == 'stop_high':
            m0.set_speed(0)
            self.pin_a.set_high()
            self.pin_b.set_high()

    def get_direction(self):
        a = self.pin_a.get_value()
        b = self.pin_b.get_value()
        return self.DIRECTION[a+b]

    def set_direction_cw(self):
        self.set_direction('cw')

    def set_directio_ccw(self):
        self.set_direction('ccw')

    def stop(self):
        self.set_direction('stop')

    def __exit__(self):
        self.pwm.set_duty_cycle(0)
        self.pwm.disable()
        self.pwm.unexport()
        self.pin_a.unexport()
        self.pin_b.unexport()

if __name__ == "__main__":

    delay = 5
    m0 = Motor(0)
    m0.set_speed(20)
    m0.set_direction('cw')
    import time
    time.sleep(delay)
    m0.stop()
    time.sleep(delay)
    m0.set_speed(20)
    m0.set_direction('ccw')
    time.sleep(delay)
    m0.stop()