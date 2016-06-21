Homepage: https://www.pololu.com/product/2738
Nazwa: MinIMU-9 v5 Gyro, Accelerometer, and Compass (LSM6DS33 and LIS3MDL Carrier)
wyprowadzenia:
				VDD: 3.3 V regulator output or low-voltage logic power supply, depending on VIN. When VIN is supplied and greater than 3.3 V, VDD is a regulated 3.3 V output that can supply up to approximately 150 mA to external components. Alternatively, when interfacing with a 2.5 V to 3.3 V system, VIN can be left disconnected and power can be supplied directly to VDD. Never supply voltage to VDD when VIN is connected, and never supply more than 3.6 V to VDD.
				VIN: This is the main 2.5 V to 5.5 V power supply connection. The SCL and SDA level shifters pull the I²C bus high bits up to this level.
				SA0: 3.3V-logic-level input to determine I²C slave addresses of the two ICs (see below). It is pulled high by default through 10 kΩ resistor. This pin is not level-shifted and is not 5V-tolerant.
				GND: The ground (0 V) connection for your power supply. Your I²C control source must also share a common ground with this board.
				SDA: Level-shifted I²C data line: HIGH is VIN, LOW is 0 V
				SCL: Level-shifted I²C clock line: HIGH is VIN, LOW is 0 V
				
Podłącznie z BBB:
MinIMU-9 v5 <---> BBB i2c2
	VDD <---> P9, 4
	VIN  -
	SA0  -
	GND <---> P9, 2
	SDA <---> P9, 20
	SCL <---> P9, 19


1. i2c2 bus setup 
	Check i2c bus speed
		[    3.212624] omap_i2c 4819c000.i2c: bus 2 rev0.11 at 400 kHz
    
		By default it is 100 kHz. Increasee the speed to 400k
			Check active overlay dtbo file name in /boot/uEnv.txt
			##BeagleBone Black: HDMI (Audio/Video) disabled:
			dtb=am335x-boneblack-emmc-overlay.dtb

			cd /boot/dtbs/`uname -r`

			cp am335x-boneblack-emmc-overlay.dtb am335x-boneblack-emmc-overlay.dtb.bkp
			dtc -I dtb -O dts -o am335x-boneblack-emmc-overlay.dts am335x-boneblack-emmc-overlay.dtb
			vi am335x-boneblack-emmc-overlay.dts
							i2c@4819c000 {
									compatible = "ti,omap4-i2c";
									#address-cells = <0x1>;
									#size-cells = <0x0>;
									ti,hwmods = "i2c3";
									reg = <0x4819c000 0x1000>;
									interrupts = <0x1e>;
									status = "okay";
									pinctrl-names = "default";
									pinctrl-0 = <0x28>;
									#clock-frequency = <0x186a0>;
									clock-frequency = <0x61a80>;
									linux,phandle = <0x89>;
									phandle = <0x89>;
			dtc -I dts -O dtb -o am335x-boneblack-emmc-overlay.dtb am335x-boneblack-emmc-overlay.dts
			reboot
			dmesg |grep i2c
	
	Setup gyro and acc from command line
		#Write CTRL9_XL = 38h // Acc X, Y, Z axes enabled
		i2cset -y 2 0x6b 0x18 0x38
		#Write CTRL1_XL = 60h // Acc = 13Hz (High Performance)
		i2cset -y 2 0x6b 0x10 0x10
		#Write INT1_CTRL = 01h // Acc Data Ready interrupt on INT1
		i2cset -y 2 0x6b   0x01

		#Write CTRL10_C = 38h // Gyro X, Y, Z axes enabled
		i2cset -y 2 0x6b 0x19 0x38
		#Write CTRL2_G = 60h // Gyro = 416Hz (High-Performance mode)
		i2cset -y 2 0x6b 0x11 0x10
		#Write INT1_CTRL = 02h // Gyro Data Ready interrupt on INT1
		i2cset -y 2 0x6b    0x02

	Reading temperature from command line
		#Read OUT_TEMP_L 0x20
		i2cget -y 2 0x6b 0x21
		#read OUT_TEMP_L 0x21
		i2cget -y 2 0x6b 0x21

		to get the value of a tempearature you need to concatenate both 8 bits values to get one 16bit 2's complement
		divide it by temperatur sensor resolution (0xF) and convert to decimal number from 2's complement binary
		
Reading the bus in project:
	To read i2c under ubuntu use smbus python library: https://pypi.python.org/pypi/smbus-cffi/
	Example code:
		#!/usr/bin/python3.4

		import smbus
		import time
		bus = smbus.SMBus(2)
		address = 0x6b

		for x in range(2):
			status = bus.read_i2c_block_data(address, 0x1E,1)
			Register = bus.read_i2c_block_data(address, 0x20,14)
			print(status, Register) 
	

I2c comunication
Accelerometer, gyroscope, termometer address: 0x6b
Magnetometer address: 0x1b

Configuration registers:
1 Write CTRL9_XL = 38h // Acc X, Y, Z axes enabled
2 Write CTRL1_XL = 10h // Acc = 13Hz (High-Performance mode)
3 Write INT1_CTRL = 01h // Acc Data Ready interrupt on INT1

1 Write CTRL10_C = 38h // Gyro X, Y, Z axes enabled
2 Write CTRL2_G = 10h // Gyro = 13Hz (High-Performance mode)
3 Write INT1_CTRL = 02h // Gyro Data Ready interrupt on INT1

Data ready status register: 
 Read STATUS_REG: 0x1E

Termometer registers
#Read OUT_TEMP_L 0x20
#read OUT_TEMP_L 0x21
Gyroscope data registers:
#Read OUTX_L_G 0x22
#Read OUTX_H_G 0x23
#Read OUTY_L_G 0x24
#Read OUTY_H_G 0x25
#Read OUTZ_L_G 0x26
#Read OUTZ_H_G 0x27
Accelerometer registers
#Read OUTX_L_XL 0x28
#Read OUTX_H_XL 0x29
#Read OUTY_L_XL 0x2A
#Read OUTY_H_XL 0x2B
#Read OUTZ_L_XL 0x2C
#Read OUTZ_H_XL 0x2D


For the accelerometer (the gyroscope is similar), the reads should be performed as follows:
1 Write CTRL9_XL = 38h // Acc X, Y, Z axes enabled
2 Write CTRL1_XL = 60h // Acc = 416Hz (High-Performance mode)
3 Write INT1_CTRL = 01h // Acc Data Ready interrupt on INT1
1 Write CTRL10_C = 38h // Gyro X, Y, Z axes enabled
2 Write CTRL2_G = 60h // Gyro = 416Hz (High-Performance mode)
3 Write INT1_CTRL = 02h // Gyro Data Ready interrupt on INT1
1 Read STATUS
2 If XLDA = 0, then go to 1
3 Read OUTX_L_XL
4 Read OUTX_H_XL
5 Read OUTY_L_XL
6 Read OUTY_H_XL
7 Read OUTZ_L_XL
8 Read OUTZ_H_XL
9 Data processing
10 Go to 1

Data are 16bits 2's complement numbers
To get proper interpretation the resolution, range and 2s complement notation needs to be taken into conciderration
Remeber tat the accelerometers measures linearr accelerations and the gyroscope reads the angular speed 





