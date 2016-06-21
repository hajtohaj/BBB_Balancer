echo BB-ADC > /sys/devices/platform/bone_capemgr/slots
cat  /sys/devices/platform/bone_capemgr/slots
dmesg|tail
cd /sys/bus/iio/devices/iio\:device0  
cat in_voltage0_raw
vin = out/4095*1.8