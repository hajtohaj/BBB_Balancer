#Enable hw modules, load device drivers, export to fs user space
#2x ADC pins for M1 and M2 curren measurements 
echo BB-ADC > /sys/devices/platform/bone_capemgr/slots

#EQEP1 module for reading encoder data
echo bone_eqep1 > /sys/devices/platform/bone_capemgr/slots

#EQEP2 module for reading encoder data
echo bone_eqep2b > /sys/devices/platform/bone_capemgr/slots

#2x pin from EHWPWM2 module for Motor speed stearing
echo BB-PWM2 >/sys/devices/platform/bone_capemgr/slots

#pins for motor direction steraing 
echo P821OUT >/sys/devices/platform/bone_capemgr/slots
while [ ! -e /sys/class/pwm/pwmchip0/export ] ;
do
 sleep 1
done

#Basic hw configuration
#M1 pwm config
echo 0 > /sys/class/pwm/pwmchip0/export
echo 1000000 > /sys/class/pwm/pwmchip0/pwm0/period
echo 0 > /sys/class/pwm/pwmchip0/pwm0/duty_cycle
echo 1 > /sys/class/pwm/pwmchip0/pwm0/enable

#M1 CW pin config
[ ! -d /sys/class/gpio/gpio36 ] && echo 36 > /sys/class/gpio/export
[ -d /sys/class/gpio/gpio36 ] && echo out > /sys/class/gpio/gpio36/direction
echo 0 > /sys/class/gpio/gpio36/value

#M1 CCW pin config
[ ! -d /sys/class/gpio/gpio62 ] && echo 62 > /sys/class/gpio/export
[ -d /sys/class/gpio/gpio62 ] && echo out > /sys/class/gpio/gpio62/direction
cat /sys/class/gpio/gpio62/value
echo 0 > /sys/class/gpio/gpio62/value

#M2 pwm config
echo 1 > /sys/class/pwm/pwmchip0/export
echo 1000000 > /sys/class/pwm/pwmchip0/pwm1/period
echo 0 > /sys/class/pwm/pwmchip0/pwm1/duty_cycle
echo 1 > /sys/class/pwm/pwmchip0/pwm1/enable

#M2 CW pin config
[ ! -d /sys/class/gpio/gpio26 ] && echo 26 > /sys/class/gpio/export
[ -d /sys/class/gpio/gpio26 ] && echo out > /sys/class/gpio/gpio26/direction
echo 0 > /sys/class/gpio/gpio26/value

#M1 CCW pin config
[ ! -d /sys/class/gpio/gpio47 ] && echo 47 > /sys/class/gpio/export
[ -d /sys/class/gpio/gpio47 ] && echo out > /sys/class/gpio/gpio47/direction
echo 0 > /sys/class/gpio/gpio47/value

#Input pin for reading position of a manual swich - (stabilization on/off)
[ ! -d /sys/class/gpio/gpio86 ] && echo 86 > /sys/class/gpio/export
[ -d /sys/class/gpio/gpio86 ] && echo in > /sys/class/gpio/gpio86/direction

#config finished - turn on green led
[ ! -d /sys/class/gpio/gpio87 ] && echo 87 > /sys/class/gpio/export
[ -d /sys/class/gpio/gpio87 ] && echo out > /sys/class/gpio/gpio87/direction
echo 1 > /sys/class/gpio/gpio87/value

