import smbus
import time


class Gyro:

    ODR = {'PowerDown': '00000000', '13Hz': '00010000', '26Hz': '00100000', '52Hz': '00110000', '104Hz': '01000000'}
    HP_FILTER_BANDWIDTH = {'0.0081Hz': '00000000', '0.0324Hz': '00010000', '2.07Hz': '00100000', '16.32Hz': '00110000'}
    AXES = {'X': '00001000', 'Y': '00010000', 'Z': '00100000', 'XYZ': '00111000'}
    FIFO_DECIMATION = {'Not in FIFO': '00000000', 'No decimation': '00001000', '2': '00010000', '3': '000110000',
                       '4': '00100000', '8': '00101000', '16': '00110000', '32': '00111000'}
    FIFO_ODR = {'Disabled': '00000000', '13Hz': '00001000', '26Hz': '00010000', '52Hz': '00011000', '104Hz': '00100000'}
    FIFO_MODE = {'Bypas': '00000000', 'FIFO': '00000001', 'Continuous': '00000110', }

    def __init__(self, bus_id, gyro_address):
        self.bus_id = bus_id
        self.gyro_address = gyro_address
        self.bus = smbus.SMBus(self.bus_id)

    def __twos_complement_to_dec16(self, raw_value):
        if raw_value >= 0x8000:
                int_val = -((65535 - raw_value) + 1)
        else:
                int_val = raw_value
        return int_val

    def __set_bits(self, register, mask, bits):
        current_value = self.bus.read_byte_data(self.gyro_address, register)
        new_value = (current_value & ~int(mask, 2)) | (int(bits, 2) & int(mask, 2))
        if current_value != new_value:
            self.bus.write_byte_data(self.gyro_address, register, new_value)

    def set_high_performance_mode(self):
        register = 0x16  # CTRL7_G
        bits = '00000000'  # G_HM_MODE
        mask = '10000000'
        self.__set_bits(register, mask, bits)

    def set_odr(self, odr):
        register = 0x11  # CTRL2_G
        bits = self.ODR[odr]  # ODR_G
        mask = '11110000'
        self.__set_bits(register, mask, bits)

    def set_hp_filter(self, bandwidth):
        register = 0x16  # CTRL7_G
        bits = self.HP_FILTER_BANDWIDTH[bandwidth]  # HPCF_G
        mask = '00110000'
        self.__set_bits(register, mask, bits)

    def enable_axes(self, axes):
        register = 0x19  # CTRL10_C
        bits = self.AXES[axes]  # Zen_G,  Yen_G,  Xen_G
        mask = '00111000'
        self.__set_bits(register, mask, bits)

    def enable_hp_filter(self):
        register = 0x16  # CTRL7_G
        bits = '01000000'  # HP_G_EN
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
        return self.__twos_complement_to_dec16(raw_data)

    def get_y(self):
        register = 0x24  # OUTX_L_G
        raw_data = self.bus.read_word_data(self.gyro_address, register)
        return self.__twos_complement_to_dec16(raw_data)

    def get_z(self):
        register = 0x26  # OUTX_L_G
        raw_data = self.bus.read_word_data(self.gyro_address, register)
        return self.__twos_complement_to_dec16(raw_data)

    def set_fifo_decimation_factor(self, decimation):
        register = 0x08  # FIFO_CTRL3
        bits = self.FIFO_DECIMATION[decimation]  # DEC_FIFO _GYRO[2:0]
        mask = '00111000'
        self.__set_bits(register, mask, bits)

    def set_fifo_odr(self, fifo_odr):
        register = 0x0A  # FIFO_CTRL5
        bits = self.FIFO_ODR[fifo_odr]  # DEC_FIFO _GYRO[2:0]
        mask = '01111000'
        self.__set_bits(register, mask, bits)

    def set_fifo_mode(self, fifo_mode):
        register = 0x0A  # FIFO_CTRL5
        bits = self.FIFO_MODE[fifo_mode]  # DEC_FIFO _GYRO[2:0]
        mask = '00000111'
        self.__set_bits(register, mask, bits)

    def get_fifo_samples_count(self):
        register = 0x3A  # FIFO_STATUS1
        bits = '0000000000000000'
        mask = '1111000000000000'
        raw_data = self.bus.read_word_data(self.gyro_address, register)
        val = (raw_data & ~int(mask, 2)) | (int(bits, 2) & int(mask, 2))
        return val

    def get_fifo_pattern(self):
        register = 0x3C  # FIFO_STATUS3
        raw_data = self.bus.read_word_data(self.gyro_address, register)
        val = raw_data
        return val

    def get_data_from_fifo(self):
        register = 0x3E  # FIFO_DATA_OUT_L
        numb_of_samples = self.get_fifo_samples_count()
        pat = []
        val = []
        for x in range(numb_of_samples):
            pat.append(self.get_fifo_pattern())
            val.append(self.__twos_complement_to_dec16(self.bus.read_word_data(self.gyro_address, register)))
        return len(val), len(pat)


if __name__ == "__main__":
    buss_address = 2
    address = 0x6b

    g = Gyro(buss_address, address)
    g.enable_axes('XYZ')
    g.set_odr('13Hz')
    g.set_hp_filter('16.32Hz')
    g.enable_hp_filter()
    g.reset_hp_filter()

    print("X: {0}, Y: {1}, Z: '{2}".format(g.get_x(), g.get_y(), g.get_z()))

    g.set_fifo_decimation_factor('No decimation')
    g.set_fifo_odr('13Hz')
    g.set_fifo_mode('Continuous')
    print(g.get_fifo_samples_count())
    print(g.get_data_from_fifo())