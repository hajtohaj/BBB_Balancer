import smbus
import time


class Gyro:

    AXES = {'X': '00001000', 'Y': '00010000', 'Z': '00100000', 'XYZ': '00111000'}
    OUTPUT_DATA_RATE_HZ = {0: '00000000', 13: '00010000', 26: '00100000', 52: '00110000', 104: '01000000'}
    FULL_SCALE_SELECTION = {125: '00000010', 245: '00000000', 500: '00000100', 1000: '00001000', 2000: '00001100'}
    HP_FILTER_BANDWIDTH_HZ = {0.0081: '00000000', 0.0324: '00010000', 2.07: '00100000', 16.32: '00110000'}

    def __init__(self, bus_id, gyro_address):
        self.bus_id = bus_id
        self.gyro_address = gyro_address
        self.bus = smbus.SMBus(self.bus_id)

    @staticmethod
    def __twos_complement_to_dec16(raw_value):
        if raw_value >= 0x8000:
            return -((65535 - raw_value) + 1)
        else:
            return raw_value

    def __set_bits(self, register, mask, bits):
        current_value = self.bus.read_byte_data(self.gyro_address, register)
        new_value = (current_value & ~int(mask, 2)) | (int(bits, 2) & int(mask, 2))
        if current_value != new_value:
            self.bus.write_byte_data(self.gyro_address, register, new_value)

    def set_full_scale_selection(self, full_scale):
        register = 0x11  # CTRL2_G
        bits = self.FULL_SCALE_SELECTION[full_scale]  # FS_G_[2:0]
        mask = '00001110'
        self.__set_bits(register, mask, bits)

    def get_full_scale_selection(self):
        register = 0x11  # CTRL2_G
        mask = '00001110'
        raw_data = self.bus.read_byte_data(self.gyro_address, register)
        fss_bits = raw_data & int(mask, 2)
        for fss in self.FULL_SCALE_SELECTION.keys():
            if int(self.FULL_SCALE_SELECTION[fss], 2) == fss_bits:
                return fss
        return -1

    def set_high_performance_mode(self):
        register = 0x16  # CTRL7_G
        bits = '00000000'  # G_HM_MODE
        mask = '10000000'
        self.__set_bits(register, mask, bits)

    def set_odr_hz(self, odr):
        register = 0x11  # CTRL2_G
        bits = self.OUTPUT_DATA_RATE_HZ[odr]  # ODR_G
        mask = '11110000'
        self.__set_bits(register, mask, bits)

    def get_odr_hz(self):
        register = 0x11  # CTRL2_G
        mask = '11110000'
        raw_data = self.bus.read_byte_data(self.gyro_address, register)
        odr_bits = raw_data & int(mask, 2)
        for odr in self.OUTPUT_DATA_RATE_HZ.keys():
            if int(self.OUTPUT_DATA_RATE_HZ[odr], 2) == odr_bits:
                return odr
        return -1

    def set_hp_filter_hz(self, bandwidth):
        register = 0x16  # CTRL7_G
        bits = self.HP_FILTER_BANDWIDTH_HZ[bandwidth]  # HPCF_G
        mask = '00110000'
        self.__set_bits(register, mask, bits)

    def enable_axes(self, axes):
        register = 0x19  # CTRL10_C
        bits = self.AXES[axes]  # Zen_G,  Yen_G,  Xen_G
        mask = '00111000'
        self.__set_bits(register, mask, bits)

    def disable_axes(self, axes):
        register = 0x19  # CTRL10_C
        bits = "{0:b}".format(~int(self.AXES[axes], 2))  # Zen_G,  Yen_G,  Xen_G
        mask = '00111000'
        self.__set_bits(register, mask, bits)

    def enable_hp_filter(self):
        register = 0x16  # CTRL7_G
        bits = '01000000'  # HP_G_EN
        mask = '01000000'
        self.__set_bits(register, mask, bits)

    def disable_hp_filter(self):
        register = 0x16  # CTRL7_G
        bits = '00000000'  # HP_G_EN
        mask = '01000000'
        self.__set_bits(register, mask, bits)

    def reset_hp_filter(self):
        register = 0x16  # CTRL7_G
        bits = '00001000'  # HP_G_RST
        mask = '00001000'
        self.__set_bits(register, mask, bits)

    def get_x(self):
        register = 0x22  # OUTX_L_G
        raw_data = self.bus.read_word_data(self.gyro_address, register)
        print(raw_data, self.__twos_complement_to_dec16(raw_data))
        return self.__twos_complement_to_dec16(raw_data)

    def get_y(self):
        register = 0x24  # OUTX_L_G
        raw_data = self.bus.read_word_data(self.gyro_address, register)
        return self.__twos_complement_to_dec16(raw_data)

    def get_z(self):
        register = 0x26  # OUTX_L_G
        raw_data = self.bus.read_word_data(self.gyro_address, register)
        return self.__twos_complement_to_dec16(raw_data)

    # def is_ev_boot(self):
    #     register = 0x1E  # STATUS_REG
    #     mask = '00001000'
    #     raw_data = self.bus.read_byte_data(self.gyro_address, register)
    #     return (raw_data & int(mask, 2)) != 0

    def is_gda(self):
        register = 0x1E  # STATUS_REG
        mask = '00000010'
        raw_data = self.bus.read_byte_data(self.gyro_address, register)
        return (raw_data & int(mask, 2)) != 0

if __name__ == "__main__":
    buss_id = 2
    address = 0x6b

    g = Gyro(buss_id, address)
    g.set_full_scale_selection(245)
    g.enable_axes('XYZ')
    g.set_odr_hz(13)
    g.set_hp_filter_hz(16.32)
    g.enable_hp_filter()
    g.reset_hp_filter()

    try:
        while 1:
            print("X: {0}, Y: {1}, Z: {2}".format(g.get_x(), g.get_y(), g.get_z()))
            time.sleep(0.035)
    except KeyboardInterrupt:
        pass
        # g.disable_hp_filter()
        # g.set_hp_filter_hz(0.0081)
        # g.set_odr_hz(0)
        # g.disable_axes('XYZ')
