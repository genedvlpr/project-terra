import time
import logging
from w1thermsensor import W1ThermSensor, NoSensorFoundError, SensorNotReadyError

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TemperatureMonitor:
    def __init__(self):
        self.sensor = None
        self.initialize_sensor()
    
    def initialize_sensor(self):
        try:
            self.sensor = W1ThermSensor()
            logger.info("DS18B20 sensor initialized successfully")
        except NoSensorFoundError:
            logger.error("No DS18B20 sensor found!")
            self.sensor = None
        except Exception as e:
            logger.error(f"Error initializing sensor: {e}")
            self.sensor = None
    
    def read_temperature(self):
        if self.sensor is None:
            logger.warning("Sensor not available")
            return None
        
        try:
            temp_c = self.sensor.get_temperature()
            temp_f = temp_c * 9.0 / 5.0 + 32.0
            return {
                'celsius': round(temp_c, 2),
                'fahrenheit': round(temp_f, 2),
                'timestamp': time.time()
            }
        except SensorNotReadyError:
            logger.warning("Sensor not ready, retrying...")
            return None
        except Exception as e:
            logger.error(f"Error reading temperature: {e}")
            return None

# Usage
if __name__ == "__main__":
    monitor = TemperatureMonitor()
    
    while True:
        temp_data = monitor.read_temperature()
        if temp_data:
            print(f"Time: {time.ctime(temp_data['timestamp'])}")
            print(f"Temperature: {temp_data['celsius']}°C / {temp_data['fahrenheit']}°F")
            print("-" * 30)
        
        time.sleep(2)
