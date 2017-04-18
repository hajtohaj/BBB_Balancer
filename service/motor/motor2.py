from gpio import Gpio
from pwm import Pwm
from eqep import Eqep


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

        self.set_encoder_zero()
        self.encoder.enable()

    def set_voltage_level(self, new_level):
        if new_level > self.MAX_VOLTAGE_LEVEL:
            new_level = self.MAX_VOLTAGE_LEVEL
        elif new_level < 0:
            new_level = self.MIN_VOLTAGE_LEVEL
        new_level *= self.___VOLTAGE_FACTOR
        self.pwm.set_duty_cycle(new_level)

    def get_voltage_level(self):
        return int(self.pwm.get_duty_cycle() / self.___VOLTAGE_FACTOR)

    def set_direction(self, direction):
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

    def get_direction(self):
        a = int(self.pin_a.get_value())
        b = int(self.pin_b.get_value())
        return (b - a) * self.DIRECTION_POLARITY

    def reverse_direction(self):
        new_direction = self.get_direction() * -1
        self.set_direction(new_direction)

    def is_direction_cw(self):
        return self.get_direction() > 0

    def is_direction_ccw(self):
        return self.get_direction() < 0

    def is_stopped(self):
        return self.get_direction() == 0

    def set_direction_cw(self):
        self.set_direction(1)

    def set_direction_ccw(self):
        self.set_direction(-1)

    def stop(self):
        self.set_direction(0)

    def set_encoder(self, value):
        self.encoder.set_counter(value)

    def set_encoder_zero(self):
        self.set_encoder(0)

    def get_encoder(self):
        return self.encoder.get_counter()

    def get_encoder_resolution(self):
        return self.ENCODER_RESOLUTION

    def set_rotation(self, value):
        if value > 0:
            if not self.is_direction_cw():
                self.set_direction_cw()
        elif value < 0:
            if not self.is_direction_ccw():
                self.set_direction_ccw()
        else:
            if not self.is_stopped():
                self.stop()
        self.set_voltage_level(int(abs(value)))

    def get_rotation(self):
        voltage_level = self.get_voltage_level()
        direction = self.get_direction()
        if direction > 0:
            return voltage_level
        elif direction < 0:
            return -1 * voltage_level
        return 0

    def change_rotation(self, change):
        current_rotation = self.get_rotation()
        self.set_rotation(current_rotation + change)

    def close(self):
        self.pwm.set_duty_cycle(0)
        self.pwm.disable()
        self.pwm.unexport()
        self.pin_a.unexport()
        self.pin_b.unexport()
        self.encoder.disable()


if __name__ == "__main__":

    m0 = Motor(1)

    delay = 1
    speeed = 10
    cw = 1
    ccw = -1

    m0.set_voltage_level(speeed)
    m0.set_direction(cw)
    import time
    time.sleep(delay)

    m0.stop()
    print(m0.get_encoder())
    time.sleep(delay)

    m0.set_voltage_level(speeed)
    m0.set_direction(ccw)
    time.sleep(delay)
    m0.stop()

    print(m0.get_encoder())
    m0.close()