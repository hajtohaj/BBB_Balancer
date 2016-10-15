

class Pwm:
    PWM_BASE_PATH = '/sys/class/pwm/pwmchip0'

    def __init__(self, pwm_id):
        self.pwm_id = pwm_id
        self.pwm_path = '/'.join([self.PWM_BASE_PATH, 'pwm' + str(self.pwm_id)])

    def _write_interface(self, interface_name, value):
        f_itf = open('/'.join([self.pwm_path, interface_name]), "w")
        f_itf.write(str(value))
        f_itf.close()

    def _read_interface(self, interface_name):
        f_itf = open('/'.join([self.pwm_path, interface_name]), "r")
        value = f_itf.read()
        return value.rstrip()

    def export(self):
        f_itf = open('/'.join([self.PWM_BASE_PATH, 'export']), "w")
        f_itf.write(str(self.pwm_id))
        f_itf.close()

    def unexport(self):
        f_itf = open('/'.join([self.PWM_BASE_PATH, 'unexport']), "w")
        f_itf.write(str(self.pwm_id))
        f_itf.close()

    def is_exported(self):
        from os import path
        return path.exists(self.pwm_path)

    def is_enabled(self):
        return self._read_interface('enable')

    def enable(self):
        self._write_interface('enable', 1)

    def disable(self):
        self._write_interface('enable', 0)

    def set_duty_cycle(self, duty_cycle):
        self._write_interface('duty_cycle', duty_cycle)

    def get_duty_cycle(self):
        return self._read_interface('duty_cycle')

    def set_period(self, period):
        self._write_interface('period', period)

    def get_period(self):
        return self._read_interface('period')

if __name__ == "__main__":

    pwm0 = Pwm(0)

    if not pwm0.is_exported():
        pwm0.export()
    if not pwm0.is_enabled():
        pwm0.enable()
    pwm0.set_period(1000000)
    print(pwm0.get_period())
    pwm0.set_duty_cycle(0)
    print(pwm0.get_duty_cycle())
    pwm0.disable()
    pwm0.unexport()
