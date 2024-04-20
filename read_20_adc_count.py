import sys
from io import StringIO
def read_adc_channel_0():

    adc_file_path = '/sys/bus/iio/devices/iio:device0/in_voltage0_raw'
    try:
        with open(adc_file_path, 'r') as adc_file:
            adc_value = adc_file.read().strip()  
            adc_value = int(adc_value)  
    except FileNotFoundError:
        print(f"ADC file {adc_file_path} not found. Make sure the path is correct.")
        adc_value = None
    except Exception as e:
        print(f"An error occurred while reading the ADC value: {e}")
        adc_value = None
    
    return adc_value
adc_values = []

for _ in range(20):
    adc_value = read_adc_channel_0()
    if adc_value is not None:
        print(f'ADC Value: {adc_value}')  
        adc_values.append(adc_value)
    else:
        print("Failed to read ADC value.")
print("Finished reading ADC values.")
