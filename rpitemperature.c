/***********************************************************
 * Filename: rpitemperature.c
 *
 * A program to capture the CPU and GPU processor 
 * temperature on the Raspberry Pi.
 *
 * Compile with the command: gcc -o rpitemperature rpitemperature.c
 *
 * Execute with the command: ./rpitemperature
 *
 **********************************************************/

#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <math.h>
#include <time.h>
#include <string.h>

int main (int argc, char **argv)
{
	float cpuTempC, cpuTempF;
	float gpuTempC, gpuTempF;
	char str_gpuTempC[40];
	
	// Get the CPU temperature.
	FILE *infile_cpuTemp;
	infile_cpuTemp = fopen("/sys/class/thermal/thermal_zone0/temp", "r");

	// Get the GPU temperature using the Raspberry Pi command, vcgencmd.
	// To get the GPU temperature, a pipe stream is created.
	FILE *infile_gpuTemp;
	infile_gpuTemp = popen("/opt/vc/bin/vcgencmd measure_temp |grep -o '[0-9;.]*'", "r");
   
	if( infile_cpuTemp == NULL  || infile_gpuTemp == NULL)
	{
		// Unable to open/read the CPU or GPU temperatures.
		// Display an error message.
		
		return 1;
	}
	else
	{
		// Get the CPU temperature.  The temperature is in Celsius (°C)
		// and is converted to degrees Fahrenheit (°F).
		fscanf(infile_cpuTemp, "%f", &cpuTempC);
		cpuTempC/=1000;
		cpuTempF = cpuTempC*(9./5.)+32.;
		
		// Get the CGU temperature.  The temperature is in Celsius (°C)
		// and is converted to degrees Fahrenheit (°F).
		while( fgets(str_gpuTempC, sizeof(str_gpuTempC), infile_gpuTemp) != NULL )
		{
			// Convert string to a floating point value.
			gpuTempC = atof(str_gpuTempC);
		}
		gpuTempF = gpuTempC*(9./5.)+32.;

		// Display the CPU or GPU temperatures.
		printf("CPU Temp: %.2f ºC / %.2f ºF\n", cpuTempC, cpuTempF);
		printf("GPU Temp: %.2f ºC / %.2f ºF\n", gpuTempC, gpuTempF);
		
		// Close the file use for the CPU temperature.
		fclose(infile_cpuTemp);
	   	// Close the file use for the GPU temperature.
		pclose(infile_gpuTemp);   
   }
   
   return 0;
}