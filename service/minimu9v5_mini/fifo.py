import smbus
import time


class Fifo:

    MODE = {'Bypass': '00000000', 'FIFO': '00000001', 'Continuous': '00000110'}
    OUTPUT_DATA_RATE_HZ = {0: '00000000', 13: '00001000', 26: '00010000', 52: '00011000', 104: '00100000',
                           208: '00101000',  416: '00110000',  833: '00111000',  1660: '01000000',  3330: '01001000',
                           6660: '01010000'}
    GYRO_DECIMATION_FACTOR = {0: '00000000', 1: '00001000', 2: '00010000', 3: '000110000',
                              4: '00100000', 8: '00101000', 16: '00110000', 32: '00111000'}
    ACC_DECIMATION_FACTOR = {0: '00000000', 1: '00000001', 2: '00000010', 3: '00000011',
                             4: '00000100', 8: '00000101', 16: '00000110', 32: '00000111'}


    def __init__(self, bus_id, address):
        self.bus_id = bus_id
        self.address = address
        self.bus = smbus.SMBus(self.bus_id)

    def enable(self, odr=104):
        f.set_gyro_decimation_factor(1)
        f.set_acc_decimation_factor(1)
        f.set_odr_hz(odr)
        f.set_mode('Continuous')

    def disable(self):
        f.set_mode('Bypass')
        f.set_gyro_decimation_factor(0)
        f.set_acc_decimation_factor(0)
        f.set_odr_hz(0)

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

    def set_gyro_decimation_factor(self, decimation=1):
        register = 0x08  # FIFO_CTRL3
        bits = self.GYRO_DECIMATION_FACTOR[decimation]  # DEC_FIFO_GYRO_[2:0]
        mask = '00111000'
        self.__set_bits(register, mask, bits)
        self.decimation_factors[0] = decimation
        self._calculate_fifo_pattern()

    def set_acc_decimation_factor(self, decimation=1):
        register = 0x08  # FIFO_CTRL3
        bits = self.ACC_DECIMATION_FACTOR[decimation]  # DEC_FIFO_XL[2:0]
        mask = '00000111'
        self.__set_bits(register, mask, bits)
        self.decimation_factors[1] = decimation
        self._calculate_fifo_pattern()

    def set_odr_hz(self, fifo_odr=104):
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

    def get_fifo_pattern_index(self):
        register = 0x3C  # FIFO_STATUS3
        return self.bus.read_word_data(self.address, register)

    def get_data(self):
        register = 0x3E  # FIFO_DATA_OUT_L
        if self.is_full():
            numb_of_samples = 4096
        else:
            numb_of_samples = self.get_sample_count()

        next_sample_idx = self.get_fifo_pattern_index() #Gx Gy Gz Ax Ay Az [0 1 2 3 4 5]

        fifo_data = []
        fifo_record = [None, None, None, None, None, None] #Gx Gy Gz Ax Ay Az

        for i in range(numb_of_samples):
            fifo_record[next_sample_idx] = self.__twos_complement_to_dec16(self.bus.read_word_data(self.address, register))
            if next_sample_idx == len(fifo_record):
                fifo_data.append(fifo_record)
                fifo_record = [None, None, None, None, None, None]  # Gx Gy Gz Ax Ay Az
            next_sample_idx = (next_sample_idx + 1) % 7

        return fifo_data

if __name__ == "__main__":
    buss_id = 2
    fifo_address = 0x6b

    f = Fifo(buss_id, fifo_address)
    f.enable(13)

    try:
        while 1:
            print(f.get_data())
            time.sleep(1)
    except KeyboardInterrupt:
        f.disable()
