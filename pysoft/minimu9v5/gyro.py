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
CTRL7_G_HP_G_RST = 0x08
CTRL7_G_HPCF_G0 = 0x10
CTRL7_G_HPCF_G1 = 0x20
CTRL7_G_HPCF_mask = ~(CTRL7_G_HPCF_G1 | CTRL7_G_HPCF_G0)
CTRL7_G_HPCF_00_0081HZ = 0x00
CTRL7_G_HPCF_00_0324HZ = CTRL7_G_HPCF_G0
CTRL7_G_HPCF_02_0700HZ = CTRL7_G_HPCF_G1
CTRL7_G_HPCF_16_3200HZ = CTRL7_G_HPCF_G1 | CTRL7_G_HPCF_G0
CTRL7_G_HP_G_EN = 0x40
CTRL7_G_G_HM_MODE = 0x80
CTRL2_G = 0x11
CTRL2_G_FS_125 = 0x02
CTRL2_G_FS_G0 = 0x04
CTRL2_G_FS_G1 = 0x08
CTRL2_G_ODR_G0 = 0x10
CTRL2_G_ODR_G1 = 0x20
CTRL2_G_ODR_G2 = 0x40
CTRL2_G_ODR_G3 = 0x80
CTRL2_G_ODR_mask = ~(CTRL2_G_ODR_G0 | CTRL2_G_ODR_G1 | CTRL2_G_ODR_G2 | CTRL2_G_ODR_G3)
CTRL2_G_ODR_13_0000HZ = CTRL2_G_ODR_G0
CTRL2_G_ODR_26_0000HZ = CTRL2_G_ODR_G1
CTRL2_G_ODR_52_0000HZ = CTRL2_G_ODR_G0 | CTRL2_G_ODR_G1
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

    def __init__(self, bus_id=2, gyro_address=0x6b):
        self.bus_id = bus_id
        self.gyro_address = gyro_address
        self.bus = smbus.SMBus(2)

    def set_bits(self, actual_value, bits):
        return actual_value | bits

    def unset_bits(self, actual_value, bits):
        return actual_value & ~bits

    def update_bits(self, actual_value, set_bits, unset_bits):
        new_value = self.set_bits(actual_value, set_bits)
        new_value = self.unset_bits(new_value, unset_bits)
        return new_value

    def update_register_bits(self, register_address, set_bits, unset_bits):
        actual_value = self.bus.read_byte_data(self.gyro_address, register_address)
        new_value = self.update_bits(actual_value, set_bits, unset_bits)
        self.bus.write_byte_data(self.gyro_address, register_address, new_value)

    def update_register_value(self, register_address, bit_mask, set_bits):
        unset_bits = ~(bit_mask | set_bits)
        self.update_register_bits(register_address, set_bits, unset_bits)

    def enable(self):
        register = CTRL10_C
        set_bits = CTRL10_C_Xen_G | CTRL10_C_Yen_G | CTRL10_C_Zen_G
        unset_bits = 0x00
        self.update_register_bits(register, set_bits, unset_bits)

    def enable_high_performance_mode(self):
        register = CTRL7_G
        set_bits = 0x00
        unset_bits = CTRL7_G_G_HM_MODE
        self.update_register_bits(register, set_bits, unset_bits)

    def disable_high_performance_mode(self):
        register = CTRL7_G
        set_bits = CTRL7_G_G_HM_MODE
        unset_bits = 0x00
        self.update_register_bits(register, set_bits, unset_bits)

    def set_hp_filter_bandwidth(self, bandwidth):
        register = CTRL7_G
        self.update_register_value(self, register, CTRL7_G_HPCF_mask, bandwidth)

    def enable_hp_filter(self):
        register = CTRL7_G
        set_bits = CTRL7_G_HP_G_EN
        unset_bits = 0x00
        self.update_register_bits(register, set_bits, unset_bits)

    def reset_hp_filter(self):
        register = CTRL7_G
        set_bits = CTRL7_G_HP_G_RST
        unset_bits = 0x00
        self.update_register_bits(register, set_bits, unset_bits)

    def set_output_data_rate(self, data_rate):
        register = CTRL2_G
        self.update_register_value(self, register, CTRL2_G_ODR_mask, data_rate)

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
    g.set_output_data_rate(CTRL2_G_ODR_13_0000HZ)
    g.set_hp_filter_bandwidth(CTRL7_G_HPCF_16_3200HZ)
    print(g.is_data_ready())
    print(g.get_X())
    print(g.get_Y())
    print(g.get_Z())