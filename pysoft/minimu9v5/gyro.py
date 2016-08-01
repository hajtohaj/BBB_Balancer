import smbus
import time

class Gyro:
    CTRL9_XL_ADDRESS = 0x18
    CTRL9_XL_ENABLE_X =  0x8
    CTRL9_XL_ENABLE_Y = 0x10
    CTRL9_XL_ENABLE_Z = 0x10

    def __init__(self, bus_id = 2, gyro_address = 0x6b):
        self.bus_id = bus_id
        self.gyro_address = gyro_address
        self.bus = smbus.SMBus(2)

    def enable(self):
        self.bus.write_byte_data(self.gyro_address, self.CTRL9_XL_ADDRESS, self.CTRL9_XL_ENABLE_X |
                                 self.CTRL9_XL_ENABLE_Y | self.CTRL9_XL_ENABLE_Z)

if __name__ == "__main__":
    g = Gyro()
    g.enable()