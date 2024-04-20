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

def calculate_rtd_voltage(adc_value):
    rtd_voltage = (adc_value + 269.12) / 2610.4
    return f"{rtd_voltage:.2f}" 

def calculate_rtd_ohm(rtd_voltage):
    rtd_voltage = float(rtd_voltage)  
    if rtd_voltage < 3.3: 
        rtd_ohm = (rtd_voltage * 2000) / (3.3 - rtd_voltage)
        return f"{rtd_ohm:.2f}" 
    return "undefined"  

def calculate_rtd_temp(rtd_ohm):
    if rtd_ohm != "undefined":
        rtd_ohm = float(rtd_ohm)
        rtd_temp = (rtd_ohm - 1000) / 3.8
        return f"{rtd_temp:.2f}"  
    return "undefined"
temperature_list = []
with open("RTD_info.txt", "w") as file:
    file.write("RTD_Voltage,ADC_Value,RTD_Ohm,RTD_Temp\n")
    for _ in range(20):
        adc_value = read_adc_channel_0()
        if adc_value is not None:
            rtd_voltage = calculate_rtd_voltage(adc_value)
            rtd_ohm = calculate_rtd_ohm(rtd_voltage)
            rtd_temp = calculate_rtd_temp(rtd_ohm)
            file.write(f"{rtd_voltage},{adc_value},{rtd_ohm},{rtd_temp}\n")  
            if rtd_temp != "undefined":
                temperature_list.append(float(rtd_temp))  
        else:
            print("Failed to read ADC value.")
if temperature_list:
    average_temperature = sum(temperature_list) / len(temperature_list)
    print(f"Average RTD Temperature: {average_temperature:.2f}")
else:
    print("No valid temperatures recorded to compute an average.")

print("Finished reading ADC values and stored in RTD_info.txt.")
