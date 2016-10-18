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
            self.encoder = Eqep(2)
        else:
            self.pwm = Pwm(0)
            self.pin_a = Gpio(36)
            self.pin_b = Gpio(62)
            self.encoder = Eqep(1)

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

        self.encoder.set_position(0)
        self.encoder.enable()

    def set_speed(self, speed):
        if speed > self.MAX_SPEED:
            speed = self.MAX_SPEED
        elif speed < 0:
            speed = self.MIN_SPEED
        speed *= self.__SPEED_FACTOR
        self.pwm.set_duty_cycle(speed)

    def get_speed(self):
        return int(self.pwm.get_duty_cycle() / self.__SPEED_FACTOR)

    def set_direction(self, direction):
        if direction == 'cw':
            self.pin_a.set_low()
            self.pin_b.set_high()
        elif direction == 'ccw':
            self.pin_a.set_high()
            self.pin_b.set_low()
        elif direction == 'stop':
            self.set_speed(0)
            self.pin_a.set_low()
            self.pin_b.set_low()
        elif direction == 'stop_high':
            self.set_speed(0)
            self.pin_a.set_high()
            self.pin_b.set_high()

    def get_direction(self):
        a = self.pin_a.get_value()
        b = self.pin_b.get_value()
        return self.DIRECTION[a+b]

    def is_direction_cw(self):
        return self.get_direction() == 'cw'

    def is_direction_ccw(self):
        return self.get_direction() == 'ccw'

    def is_stopped(self):
        return self.get_direction() == 'stop' or self.get_direction() == 'stop_high'

    def set_direction_cw(self):
        self.set_direction('cw')

    def set_direction_ccw(self):
        self.set_direction('ccw')

    def stop(self):
        self.set_direction('stop')

    def set_position(self, position):
        self.encoder.set_position(position)

    def set_position_zero(self):
        self.set_position(0)

    def get_position(self):
        return self.encoder.get_position()

    def close(self):
        self.pwm.set_duty_cycle(0)
        self.pwm.disable()
        self.pwm.unexport()
        self.pin_a.unexport()
        self.pin_b.unexport()
        self.encoder.disable()

    def set_velocity(self, new_speed):
        if new_speed > 0:
            if not self.is_direction_cw():
                self.set_direction_cw()
        elif new_speed < 0:
            if not self.is_direction_ccw():
                self.set_direction_ccw()
        else:
            if not self.is_stopped():
                self.stop()
        self.set_speed(int(abs(new_speed)))

    def get_velocity(self):
        speed = self.get_speed()
        direction = self.get_direction()
        if direction == 'cw':
            return speed
        elif direction == 'ccw':
            return -1 * speed
        return 0

    def change_velocity(self, increment):
        current_speed = self.get_velocity()
        self.set_velocity(+ increment)

if __name__ == "__main__":

    m0 = Motor(1)

    delay = 1
    speeed = 10

    m0.set_speed(speeed)
    m0.set_direction('cw')
    import time
    time.sleep(delay)

    m0.stop()
    print(m0.get_position())
    time.sleep(delay)

    m0.set_speed(speeed)
    m0.set_direction('ccw')
    time.sleep(delay)
    m0.stop()

    print(m0.get_position())
    m0.close()
