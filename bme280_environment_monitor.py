from datetime import datetime
import time
import smbus2
import bme280

# BME280 sensor address (default address)
address = 0x76

# Initialize I2C bus
bus = smbus2.SMBus(1)

# Load calibration parameters
calibration_params = bme280.load_calibration_params(bus, address)

poll_period = 60

while True:
    date = datetime.now().strftime('%Y-%m-%d')
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    try:
        data = bme280.sample(bus, address, calibration_params)
        temperature = data.temperature
        pressure = data.pressure
        humidity = data.humidity

        print(f"\r{timestamp} Temperature: {temperature:.2f}°C | Pressure: {pressure:.2f} hPa | Humidity: {humidity:.2f}%  ", end="", flush=True)

        with open(f'{date}-bme280-data.csv', 'a') as f:
            f.write(f'{timestamp},{temperature:.1f},{pressure:.1f},{humidity:.1f}\n')
        time.sleep(poll_period)
    except KeyboardInterrupt:
        print(f'{timestamp} Program stopped')
        break
    except Exception as e:
        print(f'{timestamp} Error occurred:', str(e))
        break

