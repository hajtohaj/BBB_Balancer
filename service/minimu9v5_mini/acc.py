import smbus
import time


class Acc:

    AXES = {'X': '00001000', 'Y': '00010000', 'Z': '00100000', 'YZ': '00110000', 'XYZ': '00111000'}
    OUTPUT_DATA_RATE_HZ = {0: '00000000', 13: '00010000', 26: '00100000', 52: '00110000', 104: '01000000',
                           208: '01010000', 416: '01100000', 833: '01110000', 1660: '10000000',
                           3330: '10010000', 6660: '10100000'}
    FULL_SCALE_SELECTION = {2: '00000000', 4: '00001000', 8: '00001100', 16: '00000100'}
    HP_CUTOFF_RATIO = {9: '01000000', 50: '00000000', 100: '00100000', 400: '01100000'}

    def __init__(self, bus_id, acc_address):
        self.bus_id = bus_id
        self.acc_address = acc_address
        self.bus = smbus.SMBus(self.bus_id)

    def enable(self, odr=104, f_scale=2):
        self.set_full_scale_selection(f_scale)
        self.enable_axes('XYZ')
        self.set_odr_hz(odr)

    def disable(self):
        self.set_odr_hz(0)
        self.disable_axes('XYZ')
        self.set_full_scale_selection(2)

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

    def select_lpf2(self):
        register = 0x17  # CTRL8_XL
        bits = '10000000'  # LPF2_XL_EN
        mask = '10000000'
        self.__set_bits(register, mask, bits)

    def deselect_lpf2(self):
        register = 0x17  # CTRL8_XL
        bits = '00000000'  # LPF2_XL_EN
        mask = '10000000'
        self.__set_bits(register, mask, bits)

    def select_hp_slop_filter(self):
        register = 0x17  # CTRL8_XL
        bits = '00000100'  # HP_SLOPE_XL_EN
        mask = '00000100'
        self.__set_bits(register, mask, bits)

    def deselect_hp_slop_filter(self):
        register = 0x17  # CTRL8_XL
        bits = '00000000'  # HP_SLOPE_XL_EN
        mask = '00000100'
        self.__set_bits(register, mask, bits)

    def set_hp_cutoff_ratio(self, cutoff_ratio):
        register = 0x17  # CTRL8_XL
        bits = self.HP_CUTOFF_RATIO[cutoff_ratio]  # HPCF_XL[1:0]
        mask = '01100000'
        self.__set_bits(register, mask, bits)

    def enable_hp_lpf2_filters(self):
        register = 0x58  # TAP_CFG
        bits = '00010000'  # SLOP_FDS
        mask = '00010000'
        self.__set_bits(register, mask, bits)

    def disable_hp_lpf2_filters(self):
        register = 0x58  # TAP_CFG
        bits = '00000000'  # SLOP_FDS
        mask = '00010000'
        self.__set_bits(register, mask, bits)

    def enable_embedded_functionalities(self):
        register = 0x19  # CTRL10_C
        bits = '00000100'  # FUNC_EN
        mask = '00000100'
        self.__set_bits(register, mask, bits)

    def disable_embedded_functionalities(self):
        register = 0x19  # CTRL10_C
        bits = '00000000'   # FUNC_EN
        mask = '00000100'
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

    def is_xlda(self):
        register = 0x1E  # STATUS_REG
        mask = '00000001'
        raw_data = self.bus.read_byte_data(self.acc_address, register)
        return (raw_data & int(mask, 2)) != 0

if __name__ == "__main__":
    buss_id = 2
    address = 0x6b

    a = Acc(buss_id, address)
    a.enable()

    try:
        while 1:
            print("X: {0}, Y: {1}, Z: {2}".format(a.get_x(), a.get_y(), a.get_z()))
            time.sleep(0.5)
    except KeyboardInterrupt:
        a.disable()
