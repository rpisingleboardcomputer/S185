#!/bin/bash
# -------------------------------------------------------------------
# Shell script to display the CPU & GPU temperature of a Raspberry Pi
# in a terminal/console.
# NOTE: (*) Uses the command line calculator, bc, for the temperature
#           conversion.
#           $ sudo apt-get install bc
# To make the shell script executable:
#           $ chmod u+x rpitemperature.sh
# -------------------------------------------------------------------
# Get the temperature of the CPU, in Celsius.
cpuTemp0=$(cat /sys/class/thermal/thermal_zone0/temp)
cpuTemp1=$(($cpuTemp0/1000))
cpuTemp2=$(($cpuTemp0/100))
cpuTempM=$(($cpuTemp2 % $cpuTemp1))
#  Convert the CPU temperature from Celsius to Fahrenheit.
cpuTempF1=$[(${cpuTemp1}*9/5)+32]
cpuTempF2=$[(${cpuTemp2}*9/5)+32]
cpuTempF=$(( $cpuTempF2 % $cpuTempF1 ))

# Get the temperature of the GPU, in Celsius.
gpuTemp0=$(/opt/vc/bin/vcgencmd measure_temp|cut -c6-9)
gpuTempF=$(echo "scale=2;((9/5) * $gpuTemp0) + 32" | bc)

# Display the CPU and GPU temperatures, Celsius and Fahrenheit, to the
#  terminal/console.
echo CPU Temp: $cpuTemp1"."$cpuTempM"ºC" / $cpuTempF1"."$cpuTempF"ºF"
echo GPU Temp: $gpuTemp0"ºC" / $gpuTempF"ºF"
