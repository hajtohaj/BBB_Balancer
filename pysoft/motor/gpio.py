

class Gpio:
    GPIO_BASE_PATH = '/sys/class/gpio'

    def __init__(self, gpio_id):
        self.gpio_id = gpio_id
        self.gpio_path = '/'.join([self.GPIO_BASE_PATH, 'gpio' + str(self.gpio_id)])

    def _write_interface(self, interface_name, value):
        f_itf = open('/'.join([self.gpio_path, interface_name]), "w")
        f_itf.write(str(value))
        f_itf.close()

    def _read_interface(self, interface_name):
        f_itf = open('/'.join([self.gpio_path, interface_name]), "r")
        value = f_itf.read()
        return value.rstrip()

    def is_exported(self):
        from os import path
        return path.exists(self.gpio_path)

    def export(self):
        if not self.is_exported():
            f_itf = open('/'.join([self.GPIO_BASE_PATH, 'export']), "w")
            f_itf.write(str(self.gpio_id))
            f_itf.close()

    def unexport(self):
        if self.is_exported():
            f_itf = open('/'.join([self.GPIO_BASE_PATH, 'unexport']), "w")
            f_itf.write(str(self.gpio_id))
            f_itf.close()

    def get_direction(self):
        return self._read_interface('direction')

    def set_direction(self, direction):
        self._write_interface('direction', direction)

    def set_direction_in(self):
        self.set_direction('in')

    def set_direction_out(self):
        self.set_direction('out')

    def get_value(self):
        return self._read_interface('value')

    def is_high(self):
        return (bool(self.get_value()))

    def is_low(self):
        return (not bool(self.get_value()))

    def set_value(self, new_value):
        self._write_interface('value', new_value)

    def set_high(self):
        self.set_value(1)

    def set_low(self):
        self.set_value(0)

    def togle(self):
        self.set_value(not self.get_value())

if __name__ == "__main__":

    gpio26 = Gpio(26)

    if not gpio26.is_exported():
        gpio26.export()
    print(gpio26.get_direction())
    print(gpio26.get_value())
    gpio26.unexport()
