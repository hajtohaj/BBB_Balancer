import smbus
import time


def gcd(x, y):
   if x == 0: x=1
   if y == 0: y=1
   while(y):
       x, y = y, x % y
   return x

def gcd3(x, y, z):
   return gcd(x, gcd(y,z))

def lcm(x, y):
   if x == 0: x=1
   if y == 0: y=1
   lcm = (x*y)//gcd(x,y)
   return lcm

def lcm3(x, y, z):
   return lcm(x,lcm(y,z))


class Fifo:

    MODE = {'Bypass': '00000000', 'FIFO': '00000001', 'Continuous': '00000110'}
    OUTPUT_DATA_RATE_HZ = {0: '00000000', 13: '00001000', 26: '00010000', 52: '00011000', 104: '00100000',
                           208: '00101000',  416: '00110000',  833: '00111000',  1660: '01000000',  3330: '01001000',
                           6660: '01010000'}
    GYRO_DECIMATION_FACTOR = {0: '00000000', 1: '00001000', 2: '00010000', 3: '000110000',
                              4: '00100000', 8: '00101000', 16: '00110000', 32: '00111000'}
    ACC_DECIMATION_FACTOR = {0: '00000000', 1: '00000001', 2: '00000010', 3: '00000011',
                             4: '00000100', 8: '00000101', 16: '00000110', 32: '00000111'}

    PEDO_DECIMATION_FACTOR = {0: '00000000', 1: '00001000', 2: '00010000', 3: '00011000',
                             4: '00100000', 8: '00101000', 16: '00110000', 32: '00111000'}

    def __init__(self, bus_id, address):
        self.bus_id = bus_id
        self.address = address
        self.bus = smbus.SMBus(self.bus_id)
        self.decimation_factors = [0, 0, 0] # Gyro, Acc, Pedo
        self.fifo_pattern = []

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

    def _calculate_fifo_pattern(self):
        dec_f = self.decimation_factors
        rec_size = 9 # Gx Gy Gz Ax AY AZ S1 S2 S3
        sample_index = 0
        fifo_pattern = [None for x in range(rec_size * lcm3(*dec_f))]
        for record_id in range(lcm3(*dec_f)):
            for dec_f_idx in range(len(dec_f)):
                if dec_f[dec_f_idx] and record_id % dec_f[dec_f_idx] == 0:
                    fifo_pattern[record_id * rec_size + dec_f_idx * 3 + 0] = sample_index
                    fifo_pattern[record_id * rec_size + dec_f_idx * 3 + 1] = sample_index + 1
                    fifo_pattern[record_id * rec_size + dec_f_idx * 3 + 2] = sample_index + 2
                    sample_index += 3
        self.fifo_pattern = fifo_pattern

    def _get_pattern_size(self):
        return len([x for x in self.fifo_pattern if x])

    def set_gyro_decimation_factor(self, decimation):
        register = 0x08  # FIFO_CTRL3
        bits = self.GYRO_DECIMATION_FACTOR[decimation]  # DEC_FIFO_GYRO_[2:0]
        mask = '00111000'
        self.__set_bits(register, mask, bits)
        self.decimation_factors[0] = decimation
        self._calculate_fifo_pattern()

    def set_acc_decimation_factor(self, decimation):
        register = 0x08  # FIFO_CTRL3
        bits = self.ACC_DECIMATION_FACTOR[decimation]  # DEC_FIFO_XL[2:0]
        mask = '00000111'
        self.__set_bits(register, mask, bits)
        self.decimation_factors[1] = decimation
        self._calculate_fifo_pattern()

    def set_pedo_decimation_factor(self, decimation):
        register = 0x09  # FIFO_CTRL3
        bits = self.ACC_DECIMATION_FACTOR[decimation]  # DEC_FIFO_XL[2:0]
        mask = '00111000'
        self.__set_bits(register, mask, bits)
        self.decimation_factors[2] = decimation
        self._calculate_fifo_pattern()

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

    def get_fifo_pattern_index(self):
        register = 0x3C  # FIFO_STATUS3
        return self.bus.read_word_data(self.address, register)

    # def get_data(self):
    #     pattern_size = 6
    #     register = 0x3E  # FIFO_DATA_OUT_L
    #     numb_of_samples = self.get_sample_count()
    #     if self.is_full():
    #         numb_of_samples = 4096
    #     next_sample_pattern = self.get_fifo_pattern_index()
    #     fifo_data = dict((k, []) for k in range(pattern_size))
    #     for i in range(numb_of_samples):
    #         fifo_data[next_sample_pattern].append(self.__twos_complement_to_dec16(self.bus.read_word_data(self.address, register)))
    #         next_sample_pattern = (next_sample_pattern + 1) % pattern_size
    #     return fifo_data

    def get_data(self):
        register = 0x3E  # FIFO_DATA_OUT_L
        numb_of_samples = self.get_sample_count()
        if self.is_full():
            numb_of_samples = 4096
        next_sample_pattern_idx = self.get_fifo_pattern_index()
        pattern_size = self._get_pattern_size()
        fifo_data = []
        fifo_record = [None for x in self.fifo_pattern]
        for sample_id in range(numb_of_samples):
            i = self.fifo_pattern.index(next_sample_pattern_idx) % 9
            fifo_record[i] = self.__twos_complement_to_dec16(self.bus.read_word_data(self.address, register))
            if next_sample_pattern_idx == pattern_size:
                fifo_data.append(fifo_record)
                fifo_record = [None for x in self.fifo_pattern]
            next_sample_pattern_idx = (next_sample_pattern_idx + 1) % pattern_size
        return fifo_data

if __name__ == "__main__":
    buss_id = 2
    fifo_address = 0x6b

    f = Fifo(buss_id, fifo_address)

    f.set_gyro_decimation_factor(1)
    f.set_acc_decimation_factor(1)
    f.set_odr_hz(13)
    f.set_mode('Continuous')

    try:
        while 1:
            print(f.get_data(6))
            time.sleep(1)
    except KeyboardInterrupt:
        f.set_mode('Bypass')
        f.set_gyro_decimation_factor(0)
        f.set_odr_hz(0)
