import smbus2
import bme280
import time
port = 1
address = 0x77  
bus = smbus2.SMBus(port)
calibration_params = bme280.load_calibration_params(bus, address)
data = bme280.sample(bus, address, calibration_params)
file_name = "BME280_info.txt"
with open(file_name, 'w') as file:
    for i in range(20):
        data = bme280.sample(bus, address, calibration_params)
        file.write(f"{data.temperature:.2f}\n")
        time.sleep(0.1)

print(f"done")
