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
STATUS_REG = 0x1E
STATUS_REG_XLDA = 0x01
STATUS_REG_GDA = 0x02
STATUS_REG_TDA = 0x04
STATUS_REG_EV_BOOT = 0x08
OUTX_L_G = 0x22
OUTX_H_G = 0x23
OUTY_L_G = 0x24
OUTY_H_G = 0x25
OUTZ_L_G = 0x26
OUTZ_H_G = 0x27

class Gyro:

    def __init__(self, bus_id = 2, gyro_address = 0x6b):
        self.bus_id = bus_id
        self.gyro_address = gyro_address
        self.bus = smbus.SMBus(2)

    def enable(self):
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

    def get_data_ready_status(self):
        return self.bus.read_byte_data(self.gyro_address, STATUS_REG)

    def is_data_ready(self):
        return self.get_data_ready_status() & STATUS_REG_GDA > 0

    def binary_to_int(self, raw_value):
        if (raw_value >= 0x8000):
                int_val = -((65535 - raw_value) + 1)
        else:
                int_val = raw_value
        return int_val

    def get_X(self):
        raw_data =  self.bus.read_word_data(self.gyro_address, OUTX_L_G)
        return self.binary_to_int(raw_data)

    def get_Y(self):
        raw_data =  self.bus.read_word_data(self.gyro_address, OUTY_L_G)
        return self.binary_to_int(raw_data)

    def get_Z(self):
        raw_data =  self.bus.read_word_data(self.gyro_address, OUTZ_L_G)
        return self.binary_to_int(raw_data)

if __name__ == "__main__":
    g = Gyro()
    g.enable()
    g.enable_high_performance_mode()
    g.set_output_data_rate(CTRL2_G_13HZ)
    print(g.is_data_ready())
    print(g.get_X())
    print(g.get_Y())
    print(g.get_Z())