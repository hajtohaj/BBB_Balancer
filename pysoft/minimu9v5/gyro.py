import smbus
import time

CTRL10_C = 0x19
CTRL10_C_SIGN_MOTION_EN = 0x01
CTRL10_C_PEDO_RST_STEP = 0x02
CTRL10_C_FUNC_EN = 0x04
CTRL10_C_Xen_G = 0x08
CTRL10_C_Yen_G = 0x10
CTRL10_C_Zen_G = 0x20
CTRL1_XL = 0x10
CTRL1_XL_BW_XL0 = 0x01
CTRL1_XL_BW_XL1 = 0x02
CTRL1_XL_FS_XL0 = 0x04
CTRL1_XL_FS_XL1 = 0x08
CTRL1_XL_ODR_XL0 = 0x10
CTRL1_XL_ODR_XL1 = 0x20
CTRL1_XL_ODR_XL2 = 0x40
CTRL1_XL_ODR_XL3 = 0x80

class Gyro:

    def __init__(self, bus_id = 2, gyro_address = 0x6b):
        self.bus_id = bus_id
        self.gyro_address = gyro_address
        self.bus = smbus.SMBus(2)

    def enable(self):
        self.bus.write_byte_data(self.gyro_address, CTRL10_C, CTRL10_C_Xen_G | CTRL10_C_Yen_G | CTRL10_C_Zen_G)

if __name__ == "__main__":
    g = Gyro()
    g.enable()