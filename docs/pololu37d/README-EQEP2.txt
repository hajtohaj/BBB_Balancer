https://www.pololu.com/product/2822
TG-EQEP2.dts
# Based on https://github.com/Teknoman117/beaglebot.git

# git clone https://github.com/Teknoman117/beaglebot.git

# cd beaglebot/encoders/dts/

# cp bone_eqep2b-00A0.dtbo /lib/firmware/

echo TG-EQEP2.dts > /sys/devices/platform/bone_capemgr/slots
cat /sys/devices/platform/bone_capemgr/slots
cd /sys/devices/platform/ocp/48304000.epwmss/48304180.eqep
cat enabled 
cat position 
echo -5 > /sys/devices/platform/bone_capemgr/slots


37D
	Red:	motor power (connects to one motor terminal)
	Black:	motor power (connects to the other motor terminal)
	Green:	encoder GND
	Blue:	encoder Vcc (3.5 – 20 V)
	Yellow:	encoder A output
	White:	encoder B output

BBB
	EQEP2A  P8_12 filoetowy
	EQEP2B  P8_11 pomaranczowy
	GND     P9_1 szary
	DC_5V   P9_5 czerwony

Po³¹czenie: (wymagany dzielnik napiêcia (0.66)  )
Func 	 BBB   <--->   37D
A:		P8_12  <--->  Yellow
B:		P8_11  <--->  White
GND:	P9_1   <--->  Green
5V:		P9_5   <--->  Blue