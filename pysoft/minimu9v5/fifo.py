import smbus
import time


class Fifo:

    MODE = {'Bypass': '00000000', 'FIFO': '00000001', 'Continuous': '00000110'}
    OUTPUT_DATA_RATE_HZ = {0: '00000000', 13: '00001000', 26: '00010000', 52: '00011000', 104: '00100000'}
    GYRO_DECIMATION_FACTOR = {0: '00000000', 1: '00001000', 2: '00010000', 3: '000110000',
                              4: '00100000', 8: '00101000', 16: '00110000', 32: '00111000'}
    ACC_DECIMATION_FACTOR = {0: '00000000', 1: '00000001', 2: '00000010', 3: '00000011',
                             4: '00000100', 8: '00000101', 16: '00000110', 32: '00000111'}

    def __init__(self, bus_id, address):
        self.bus_id = bus_id
        self.address = address
        self.bus = smbus.SMBus(self.bus_id)

    @staticmethod
    def __twos_complement_to_dec16(raw_value):
        if raw_value >= 0x8000:
            return -((65535 - raw_value) + 1)
        else:
            return raw_value

    def __set_bits(self, register, mask, bits):
        current_value = self.bus.read_byte_data(self.address, register)
        new_value = (current_value & ~int(mask, 2)) | (int(bits, 2) & int(mask, 2))
        if current_value != new_value:
            self.bus.write_byte_data(self.address, register, new_value)

    def set_gyro_decimation_factor(self, decimation):
        register = 0x08  # FIFO_CTRL3
        bits = self.GYRO_DECIMATION_FACTOR[decimation]  # DEC_FIFO_GYRO_[2:0]
        mask = '00111000'
        self.__set_bits(register, mask, bits)

    def set_acc_decimation_factor(self, decimation):
        register = 0x08  # FIFO_CTRL3
        bits = self.ACC_DECIMATION_FACTOR[decimation]  # DEC_FIFO_XL[2:0]
        mask = '00000111'
        self.__set_bits(register, mask, bits)

    def set_odr_hz(self, fifo_odr):
        register = 0x0A  # FIFO_CTRL5
        bits = self.OUTPUT_DATA_RATE_HZ[fifo_odr]  # ODR_FIFO_[3:0]
        mask = '01111000'
        self.__set_bits(register, mask, bits)

    def set_mode(self, fifo_mode):
        register = 0x0A  # FIFO_CTRL5
        bits = self.MODE[fifo_mode]  # FIFO_MODE_[2:0]
        mask = '00000111'
        self.__set_bits(register, mask, bits)

    def get_sample_count(self):
        register = 0x3A  # FIFO_STATUS1
        bits = '0000000000000000'
        mask = '1111000000000000'
        raw_data = self.bus.read_word_data(self.address, register)
        val = (raw_data & ~int(mask, 2)) | (int(bits, 2) & int(mask, 2))
        return val

    def is_fth(self):
        register = 0x3B  # FIFO_STATUS2
        mask = '10000000'
        raw_data = self.bus.read_byte_data(self.address, register)
        return (raw_data & int(mask, 2)) != 0

    def is_over_run(self):
        register = 0x3B  # FIFO_STATUS1
        mask = '01000000'
        raw_data = self.bus.read_byte_data(self.address, register)
        return (raw_data & int(mask, 2)) != 0

    def is_full(self):
        register = 0x3B  # FIFO_STATUS1
        mask = '00100000'
        raw_data = self.bus.read_byte_data(self.address, register)
        return (raw_data & int(mask, 2)) != 0

    def is_empty(self):
        register = 0x3B  # FIFO_STATUS1
        mask = '00010000'
        raw_data = self.bus.read_byte_data(self.address, register)
        return (raw_data & int(mask, 2)) != 0

    def get_fifo_pattern(self):
        register = 0x3C  # FIFO_STATUS3
        return self.bus.read_word_data(self.address, register)

    def get_data(self):
        register = 0x3E  # FIFO_DATA_OUT_L
        if self.is_full():
            numb_of_samples = 4096
        else:
            numb_of_samples = self.get_sample_count()
        fifo_data = dict()
        for sample_idx in range(numb_of_samples):
            fifo_pattern = self.get_fifo_pattern()
            if fifo_pattern in fifo_data.keys():
                fifo_data[fifo_pattern] = (fifo_data[fifo_pattern][0] + self.__twos_complement_to_dec16(
                    self.bus.read_word_data(self.address, register)), fifo_data[fifo_pattern][1] + 1)
            else:
                fifo_data[fifo_pattern] = (self.__twos_complement_to_dec16(
                    self.bus.read_word_data(self.address, register)), 1)
        return fifo_data

    def disable(self):
        self.set_mode('Bypass')
        self.set_gyro_decimation_factor(0)
        self.set_odr_hz(0)

if __name__ == "__main__":
    buss_id = 2
    fifo_address = 0x6b

    f = Fifo(buss_id, fifo_address)

    f.set_gyro_decimation_factor(1)
    f.set_odr_hz(26)
    f.set_mode('Continuous')

    try:
        while 1:
            print(f.get_data())
            time.sleep(1)
    except KeyboardInterrupt:
        f.disable(0)
