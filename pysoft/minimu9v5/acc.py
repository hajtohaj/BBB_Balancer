import smbus
import time


class Acc:

    AXES = {'X': '00001000', 'Y': '00010000', 'Z': '00100000', 'XYZ': '00111000'}
    OUTPUT_DATA_RATE_HZ = {0: '00000000', 13: '00010000', 26: '00100000', 52: '00110000', 104: '01000000',
                           208: '01010000', 416: '01100000', 833: '01110000', 1660: '10000000',
                           3330: '10010000', 6660: '10100000'}
    FULL_SCALE_SELECTION = {2: '00000000', 4: '00001000', 8: '00001100', 16: '00000100'}
    # HP_FILTER_BANDWIDTH_HZ = {0.0081: '00000000', 0.0324: '00010000', 2.07: '00100000', 16.32: '00110000'}

    def __init__(self, bus_id, acc_address):
        self.bus_id = bus_id
        self.acc_address = acc_address
        self.bus = smbus.SMBus(self.bus_id)

    @staticmethod
    def __twos_complement_to_dec16(raw_value):
        if raw_value >= 0x8000:
            return -((65535 - raw_value) + 1)
        else:
            return raw_value

    def __set_bits(self, register, mask, bits):
        current_value = self.bus.read_byte_data(self.acc_address, register)
        new_value = (current_value & ~int(mask, 2)) | (int(bits, 2) & int(mask, 2))
        if current_value != new_value:
            self.bus.write_byte_data(self.acc_address, register, new_value)

    def set_full_scale_selection(self, full_scale):
        register = 0x10  # CTRL1_XL
        bits = self.FULL_SCALE_SELECTION[full_scale]  # FS_XL_[1:0]
        mask = '00001100'
        self.__set_bits(register, mask, bits)

    def get_full_scale_selection(self):
        register = 0x10  # CTRL1_XL
        mask = '00001100'
        raw_data = self.bus.read_byte_data(self.acc_address, register)
        fss_bits = raw_data & int(mask, 2)
        for fss in self.FULL_SCALE_SELECTION.keys():
            if int(self.FULL_SCALE_SELECTION[fss], 2) == fss_bits:
                return fss
        return -1

    def set_high_performance_mode(self):
        register = 0x15  # CTRL6_C
        bits = '00000000'  # XL_HM_MODE
        mask = '00010000'
        self.__set_bits(register, mask, bits)

    def set_odr_hz(self, odr):
        register = 0x10  # CTRL1_XL
        bits = self.OUTPUT_DATA_RATE_HZ[odr]  # ODR_G
        mask = '11110000'
        self.__set_bits(register, mask, bits)

    def get_odr_hz(self):
        register = 0x10  # CTRL2_G
        mask = '11110000'
        raw_data = self.bus.read_byte_data(self.acc_address, register)
        odr_bits = raw_data & int(mask, 2)
        for odr in self.OUTPUT_DATA_RATE_HZ.keys():
            if int(self.OUTPUT_DATA_RATE_HZ[odr], 2) == odr_bits:
                return odr
        return -1

    def enable_axes(self, axes):
        register = 0x18  # CTRL9_XL
        bits = self.AXES[axes]  # Zen_XL,  Yen_XL,  Xen_XL
        mask = '00111000'
        self.__set_bits(register, mask, bits)

    def disable_axes(self, axes):
        register = 0x18  # CTRL9_XL
        bits = "{0:b}".format(~int(self.AXES[axes], 2))  # Zen_G,  Yen_G,  Xen_G
        mask = '00111000'
        self.__set_bits(register, mask, bits)

    def get_x(self):
        register = 0x28  # OUTX_L_XL
        raw_data = self.bus.read_word_data(self.acc_address, register)
        return self.__twos_complement_to_dec16(raw_data)

    def get_y(self):
        register = 0x2A  # OUTY_L_XL
        raw_data = self.bus.read_word_data(self.acc_address, register)
        return self.__twos_complement_to_dec16(raw_data)

    def get_z(self):
        register = 0x2C  # OUTZ_L_XL
        raw_data = self.bus.read_word_data(self.acc_address, register)
        return self.__twos_complement_to_dec16(raw_data)

    def is_tda(self):
        register = 0x1E  # STATUS_REG
        mask = '00000100'
        raw_data = self.bus.read_byte_data(self.gyro_address, register)
        return (raw_data & int(mask, 2)) != 0

if __name__ == "__main__":
    buss_id = 2
    address = 0x6b

    a = Acc(buss_id, address)
    a.set_full_scale_selection(2)
    a.enable_axes('XYZ')
    a.set_odr_hz(13)

    try:
        while 1:
            print("X: {0}, Y: {1}, Z: {2}".format(a.get_x(), a.get_y(), a.get_z()))
            time.sleep(0.5)
    except KeyboardInterrupt:
        a.set_odr_hz(0)
        a.disable_axes('XYZ')
        a.set_full_scale_selection(2)