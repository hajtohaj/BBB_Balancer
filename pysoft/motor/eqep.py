
class Eqep:
    EQEP1_PATH = '/sys/devices/platform/ocp/48304000.epwmss/48304180.eqep'
    EQEP2_PATH = '/sys/devices/platform/ocp/48302000.epwmss/48302180.eqep'
    EQEP = {1:EQEP1_PATH, 2:EQEP2_PATH}

    def __init__(self, eqep_id):
        self.eqep_id = eqep_id

    def _write_interface(self, interface_name, value):
        f_itf = open('/'.join([self.EQEP[self.eqep_id], interface_name]), "w")
        f_itf.write(str(value))
        f_itf.close()

    def _read_interface(self, interface_name):
        f_itf = open('/'.join([self.EQEP[self.eqep_id], interface_name]), "r")
        value = f_itf.read()
        return value.rstrip()

    def is_enabled(self):
        return int(self._read_interface('enabled'))

    def enable(self):
        self._write_interface('enabled', 1)

    def disable(self):
        self._write_interface('enabled', 0)

    def set_position(self, position):
        self._write_interface('position', position)

    def get_position(self):
        return self._read_interface('position')

if __name__ == "__main__":

    eqep1 = Eqep(1)

    if not eqep1.is_enabled():
        eqep1.enable()
    print(eqep1.get_position())
    eqep1.set_position(12345)
    print(eqep1.get_position())
    eqep1.set_position()
    eqep1.disable()