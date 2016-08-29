import smbus
import time



class Gyro:

    G_ODR = {'PowerDown': '00000000', '13Hz': '00010000', '26Hz': '00100000', '52Hz': '00110000', '104Hz': '01000000'}
    HP_FILTER_BANDWIDTH = {'0.0081Hz': '00000000', '0.0324Hz':'00010000', '2.07Hz': '00100000', '16.32Hz': '00110000'}
    AXES = {'X': '00001000', 'Y': '00010000', 'Z': '00100000', 'XYZ': '00111000'}

    def __init__(self, bus_id, gyro_address):
        self.bus_id = bus_id
        self.gyro_address = gyro_address
        self.bus = smbus.SMBus(self.bus_id)

    def set_high_performance_mode(self):
        register = 0x16  # CTRL7_G
        bits = '00000000'  # G_HM_MODE
        mask = '01111111'
        new_value = (self.bus.read_byte_data(self.gyro_address, register) & int(mask, 2)) | int(bits, 2)
        self.bus.write_byte_data(self.gyro_address, register, new_value)

    def set_ODR(self, odr):
        register = 0x11  # CTRL2_G
        bits = self.G_ODR[odr]  # ODR_G
        mask = '00001111'
        new_value = (self.bus.read_byte_data(self.gyro_address, register) & int(mask, 2)) | int(bits, 2)
        self.bus.write_byte_data(self.gyro_address, register, new_value)

    def set_hp_filter(self, bandwidth):
        register = 0x16  # CTRL7_G
        bits = self.HP_FILTER_BANDWIDTH[bandwidth]  # HPCF_G
        mask = '11001111'
        new_value = (self.bus.read_byte_data(self.gyro_address, register) & int(mask, 2)) | int(bits, 2)
        self.bus.write_byte_data(self.gyro_address, register, new_value)

    def enable_axes(self, axes):
        register = 0x19  # CTRL10_C
        bits = self.AXES[axes]  # Zen_G,  Yen_G,  Xen_G
        mask = '11000111'
        new_value = (self.bus.read_byte_data(self.gyro_address, register) & int(mask, 2)) | int(bits, 2)
        self.bus.write_byte_data(self.gyro_address, register, new_value)

    def enable_hp_filter(self):
        register = 0x16  # CTRL7_G
        bits = '01000000'  # HP_G_EN
        mask = '10111111'
        new_value = (self.bus.read_byte_data(self.gyro_address, register) & int(mask, 2)) | int(bits, 2)
        self.bus.write_byte_data(self.gyro_address, register, new_value)

    def reset_hp_filter(self):
        register = 0x16  # CTRL7_G
        bits = '00001000'  # HP_G_RST
        mask = '11110111'
        new_value = (self.bus.read_byte_data(self.gyro_address, register) & int(mask, 2)) | int(bits, 2)
        self.bus.write_byte_data(self.gyro_address, register, new_value)



if __name__ == "__main__":
    buss_address = 2
    gyro_address = 0x6b

    g = Gyro(buss_address, gyro_address)
    g.enable_axes('XYZ')
    g.set_output_data_rate('13Hz')
    g.set_hp_filter('16.32Hz')
    g.enable_hp_filter()
    g.reset_hp_filter()

