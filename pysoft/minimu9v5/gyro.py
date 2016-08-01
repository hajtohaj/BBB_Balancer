import smbus
import time

CTRL10_C = 0x19
CTRL10_C_SIGN_MOTION_EN = 0x01
CTRL10_C_PEDO_RST_STEP = 0x02
CTRL10_C_FUNC_EN = 0x04
CTRL10_C_Xen_G = 0x08
CTRL10_C_Yen_G = 0x10
CTRL10_C_Zen_G = 0x20
CTRL7_G = 0x16
CTRL7_G_G_HM_MODE = 0x80
CTRL2_G = 0x11
CTRL2_G_FS_125 = 0x02
CTRL2_G_FS_G0 = 0x04
CTRL2_G_FS_G1 = 0x08
CTRL2_G_ODR_G0 = 0x10
CTRL2_G_ODR_G1 = 0x20
CTRL2_G_ODR_G2 = 0x40
CTRL2_G_ODR_G3 = 0x80
CTRL2_G_13HZ = CTRL2_G_ODR_G0
CTRL2_G_26HZ = CTRL2_G_ODR_G1
CTRL2_G_52HZ = CTRL2_G_ODR_G0 | CTRL2_G_ODR_G1

class Gyro:

    def __init__(self, bus_id = 2, gyro_address = 0x6b):
        self.bus_id = bus_id
        self.gyro_address = gyro_address
        self.bus = smbus.SMBus(2)

    def device_enable(self):
        self.bus.write_byte_data(self.gyro_address, CTRL10_C, CTRL10_C_Xen_G | CTRL10_C_Yen_G | CTRL10_C_Zen_G)

    def enable_high_performance_mode(self):
        status = self.bus.read_byte_data(self.gyro_address, CTRL7_G)
        self.bus.write_byte_data(self.gyro_address, CTRL7_G, CTRL7_G_G_HM_MODE | status)

    def disable_high_performance_mode(self):
        status = self.bus.read_byte_data(self.gyro_address, CTRL7_G)
        self.bus.write_byte_data(self.gyro_address, CTRL7_G, (~ CTRL7_G_G_HM_MODE) | status)

    def set_output_data_rate(self, data_rate=CTRL2_G_13HZ):
        status = self.bus.read_byte_data(self.gyro_address, CTRL2_G)
        self.bus.write_byte_data(self.gyro_address, CTRL2_G, data_rate | (0xf & status))

if __name__ == "__main__":
    g = Gyro()
    g.device_enable()
    g.enable_high_performance_mode()
    g.set_output_data_rate(CTRL2_G_13HZ)