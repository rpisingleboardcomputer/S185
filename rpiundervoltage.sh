#!/bin/bash

# This bash script outputs the status of your Raspberry Pi and checks whether
#  you are being throttled for undervoltage and gives you your temperature.
#  NOTE: (1) To make the shell script executable:
#            chmod u+x undervoltage.sh

#https://elinux.org/RPI_vcgencmd_usage

# pi@raspberrypi:~ $ vcgencmd get_throttled
#  0: under-voltage
#  1: arm frequency capped
#  2: currently throttled
# 16: under-voltage has occurred
# 17: arm frequency capped has occurred
# 18: throttling has occurred

 #  0: under-voltage (0xX0001)
 #  1: arm frequency capped (0xX0002 or 0xX0003 with under-voltage)
 #  2: currently throttled (0xX0004 or 0xX0005 with under-voltage)

 # 16: under-voltage has occurred (0x1000X)
 # 17: arm frequency capped has occurred (0x2000X or 0x3000X also under-voltage
 #     occurred)
 # 18: throttling has occurred (0x4000X or 0x5000X also under-voltage occurred)

 # under-voltage occurs when voltage drops below 4.63V. The Raspberry Pi is 
 #   throttled
 # arm frequency capped occurs with temp > 80'C
 # over-temperature occurs with temp > 85'C. The Raspberry Pi is throttled

 # Throttling removes turbo mode, which reduces core voltage, and sets arm and 
 #  gpu frequencies to non-turbo value.
 # Capping just limits the arm frequency (somewhere between 600MHz and 1200MHz)
 #  to try to avoid throttling.
 # If you are throttled and not under-voltage then you can assume 
 #  over-temperature. (confirm with vcgencmd measure_temp).


# Shows how much memory is split between the CPU (arm) and GPU. 
echo "Memory split between the CPU and GPU:"
vcgencmd get_mem arm && vcgencmd get_mem gpu

# Output current configuration
echo ""
echo "Raspberry Pi Configuration:"
vcgencmd get_config int | egrep "(arm|core|gpu|sdram)_freq|over_volt"

# Measure Clock Speeds
echo ""
echo "Measured Clock Frequencies:"
for src in arm core h264 isp v3d;
    do echo -e "   $src: \t$(vcgencmd measure_clock $src)";
done

# Measure Volts
echo ""
echo "Measured Voltages:"
for id in core sdram_c sdram_i sdram_p;
    do echo -e "   $id:\t$(vcgencmd measure_volts $id)";
done

# Measure Temperature
echo ""
echo "The Measured core Temperature of the SoC:"
SoCTemp_string=$(vcgencmd measure_temp)
SoCTemp=${SoCTemp_string:5:-2}
echo SoC Temperature: $SoCTemp"ºC"

# See if we are being throttled
echo ""
echo "Checking if the Raspberry Pi is being throttled..."
throttled="$(vcgencmd get_throttled)"
#echo -e "$throttled"
if [[ $throttled != "throttled=0x0" ]]; then
   echo "WARNING:  You are being throttled."
   echo "          This is likely because you are undervoltaged."
   echo "          Please connect your Raspberry Pi to a better power supply!"
else
   echo "You are *NOT* being throttled."
	echo -e "$throttled"
fi

# Show the firmware version.
echo ""
echo "The Firmware Version:"
vcgencmd version
