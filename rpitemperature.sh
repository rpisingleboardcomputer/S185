#!/bin/bash
# -------------------------------------------------------------
# Script to display the CPU & GPU temperature of a Raspberry Pi
# in the console.
# NOTE: 	(1)	To make the shell script executable: 
#					chmod u+x rpitemperature.sh
#			(2)	Uses a command line calculator, bc.
#					sudo apt-get install bc
# -------------------------------------------------------------
# Get the temperature of the CPU, in Celsius
cpuTemp0=$(cat /sys/class/thermal/thermal_zone0/temp)
cpuTemp1=$(($cpuTemp0/1000))
cpuTemp2=$(($cpuTemp0/100))
cpuTempM=$(($cpuTemp2 % $cpuTemp1))
#  Convert the CPU temperature to Fahrenheit
cpuTempF1=$[(${cpuTemp1}*9/5)+32]
cpuTempF2=$[(${cpuTemp2}*9/5)+32]
cpuTempF=$(( $cpuTempF2 % $cpuTempF1 ))

# Get the temperature of the GPU, in Celsius
#gpuTemp0=$(/opt/vc/bin/vcgencmd measure_temp)
#gpuTemp0=${gpuTemp0//\'/º}
#gpuTemp0=${gpuTemp0//temp=/}
gpuTemp0=$(/opt/vc/bin/vcgencmd measure_temp|cut -c6-9)
gpuTempF=$(echo "scale=2;((9/5) * $gpuTemp0) + 32" | bc)

# Display the CPU and GPU temperature to the console
echo CPU Temp: $cpuTemp1"."$cpuTempM"ºC" / $cpuTempF1"."$cpuTempF"ºF"
echo GPU Temp: $gpuTemp0"ºC" / $gpuTempF"ºF"
