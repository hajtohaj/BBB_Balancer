from gpio import Gpio
from pwm import Pwm
from eqep import Eqep
import time


class Motor:

    MAX_VOLTAGE_LEVEL = 100
    MIN_VOLTAGE_LEVEL = 0

    ENCODER_RESOLUTION = 1200

    ___VOLTAGE_FACTOR = 10000

    DIRECTION_POLARITY = 1

    def __init__(self, motor_id, polarity=1):
        self.motor_id = motor_id

        if polarity < 0:
            self.DIRECTION_POLARITY = -1

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
        self.pwm.set_period(self.MAX_VOLTAGE_LEVEL * self.___VOLTAGE_FACTOR)
        self.pwm.set_duty_cycle(0)
        self.pwm.enable()

        self.pin_a.export()
        self.pin_a.set_direction_out()
        self.pin_a.set_low()

        self.pin_b.export()
        self.pin_b.set_direction_out()
        self.pin_b.set_low()

        self.set_encoder(0)
        self.encoder.enable()

    def close(self):
        self.pwm.set_duty_cycle(0)
        self.pwm.disable()
        self.pwm.unexport()
        self.pin_a.unexport()
        self.pin_b.unexport()
        self.encoder.disable()

    def __set_absolute_v_level(self, new_level):
        if new_level > self.MAX_VOLTAGE_LEVEL:
            new_level = self.MAX_VOLTAGE_LEVEL
        elif new_level < 0:
            new_level = self.MIN_VOLTAGE_LEVEL
        new_level *= self.___VOLTAGE_FACTOR
        self.pwm.set_duty_cycle(new_level)

    def __get_absolute_v_level(self):
        return int(self.pwm.get_duty_cycle() / self.___VOLTAGE_FACTOR)

    def __set_direction(self, direction):
        direction *= self.DIRECTION_POLARITY
        if direction > 0:
            self.pin_a.set_low()
            self.pin_b.set_high()
        elif direction < 0:
            self.pin_a.set_high()
            self.pin_b.set_low()
        else:
            self.pin_a.set_low()
            self.pin_b.set_low()

    def __get_direction(self):
        a = int(self.pin_a.get_value())
        b = int(self.pin_b.get_value())
        return (b - a) * self.DIRECTION_POLARITY

    def set_encoder(self, value):
        self.encoder.set_position(value)

    def get_encoder(self):
        return self.encoder.get_position()

    def get_radians(self):
        print(self.get_encoder())
        return self.get_encoder() * 2 * 3.14159265359 / self.ENCODER_RESOLUTION

    def set_voltage(self, level):
        self.__set_direction(level)
        self.__set_absolute_v_level(int(abs(level)))

    def get_voltage(self):
        return self.__get_absolute_v_level() * self.__get_direction()


if __name__ == "__main__":

    m0 = Motor(0)
    voltage_level = 15

    try:
        while 1:
            print(m0.get_radians())
            m0.set_velocity(voltage_level)
            time.sleep(0.25)


    except KeyboardInterrupt:
        m0.close()
