#!/usr/bin/env python3

import board
import adafruit_dht
import os
import glob
import time
import json
import traceback

# --- Sensor Configuration ---
SENSOR_ID = "RPI_SENSOR_STATION"

# DHT11 Configuration
DHT_PIN = board.D4  # GPIO4, Physical pin 7
DHT_SENSOR_TYPE = adafruit_dht.DHT11

# DS18B20 Configuration (One-Wire)
ONE_WIRE_BASE_DIR = '/sys/bus/w1/devices/'

# Initialize DHT11 device
dhtDevice = adafruit_dht.DHT11(DHT_PIN)

def find_ds18b20_sensors():
    """Find all connected DS18B20 sensors"""
    try:
        device_folders = glob.glob(ONE_WIRE_BASE_DIR + '28*')
        sensors = {}
        for folder in device_folders:
            sensor_id = os.path.basename(folder)
            sensors[sensor_id] = folder + '/w1_slave'
        return sensors
    except Exception as e:
        print(f"Error finding DS18B20 sensors: {e}")
        return {}

def read_ds18b20_raw(device_file):
    """Read raw data from DS18B20 sensor"""
    try:
        with open(device_file, 'r') as f:
            lines = f.readlines()
        return lines
    except Exception as e:
        print(f"Error reading DS18B20 raw data: {e}")
        return None

def get_ds18b20_temperature(device_file):
    """Read temperature from specific DS18B20 sensor"""
    try:
        lines = read_ds18b20_raw(device_file)
        if lines is None:
            return None
            
        # Wait for valid data
        retries = 0
        while lines[0].strip()[-3:] != 'YES' and retries < 5:
            time.sleep(0.2)
            lines = read_ds18b20_raw(device_file)
            retries += 1
            if lines is None:
                return None
        
        if lines[0].strip()[-3:] == 'YES':
            equals_pos = lines[1].find('t=')
            if equals_pos != -1:
                temp_string = lines[1][equals_pos+2:]
                temperature_c = float(temp_string) / 1000.0
                return temperature_c
        
        return None
    except Exception as e:
        print(f"Error processing DS18B20 data: {e}")
        return None

def get_dht11_data():
    """Reads DHT11 sensor and returns data"""
    data = {
        "temperature_c": None,
        "humidity": None,
        "status": "ERROR"
    }

    try:
        temperature_c = dhtDevice.temperature
        humidity = dhtDevice.humidity

        if temperature_c is not None and humidity is not None:
            data = {
                "temperature_c": round(temperature_c, 1),
                "temperature_f": round(temperature_c * (9 / 5) + 32, 1),
                "humidity": round(humidity, 1),
                "status": "OK"
            }
        else:
            data["status"] = "READ_FAILED"

    except RuntimeError as error:
        data["status"] = "RUNTIME_ERROR"
        data["message"] = str(error)
    except Exception as e:
        data["status"] = "UNEXPECTED_ERROR"
        data["message"] = str(e)

    return data

def get_all_sensor_data():
    """Read data from all sensors and return combined JSON"""
    # Find DS18B20 sensors
    ds18b20_sensors = find_ds18b20_sensors()
    
    # Read DHT11 data
    dht_data = get_dht11_data()
    
    # Read DS18B20 data
    ds18b20_data = {}
    for sensor_id, device_file in ds18b20_sensors.items():
        temp_c = get_ds18b20_temperature(device_file)
        if temp_c is not None:
            ds18b20_data[sensor_id] = {
                "temperature_c": round(temp_c, 2),
                "temperature_f": round(temp_c * (9 / 5) + 32, 2),
                "status": "OK"
            }
        else:
            ds18b20_data[sensor_id] = {
                "temperature_c": None,
                "temperature_f": None,
                "status": "READ_FAILED"
            }
    
    # Combine all data
    combined_data = {
        "id": SENSOR_ID,
        "timestamp": time.time(),
        "dht11": dht_data,
        "ds18b20": ds18b20_data,
        "sensor_count": {
            "dht11": 1,
            "ds18b20": len(ds18b20_sensors)
        }
    }
    
    return combined_data

def setup_one_wire():
    """Enable One-Wire interface if not already enabled"""
    try:
        # Check if One-Wire devices are detected
        if not glob.glob(ONE_WIRE_BASE_DIR + '28*'):
            print("⚠️  No DS18B20 sensors found. Please ensure:")
            print("   1. One-Wire is enabled in raspi-config")
            print("   2. DS18B20 is properly wired (VCC, GND, DATA)")
            print("   3. 4.7kΩ pull-up resistor between VCC and DATA")
            return False
        return True
    except Exception as e:
        print(f"Error setting up One-Wire: {e}")
        return False

if __name__ == '__main__':
    print("--- Raspberry Pi Multi-Sensor Station ---")
    print("Initializing sensors...")
    
    # Setup One-Wire interface
    one_wire_ready = setup_one_wire()
    
    if one_wire_ready:
        ds18b20_sensors = find_ds18b20_sensors()
        print(f"✅ Found {len(ds18b20_sensors)} DS18B20 sensor(s)")
        for sensor_id in ds18b20_sensors.keys():
            print(f"   - {sensor_id}")
    else:
        print("❌ No DS18B20 sensors detected")
    
    print("✅ DHT11 sensor initialized")
    print("-" * 50)

    try:
        while True:
            # Read all sensors
            sensor_data = get_all_sensor_data()
            
            # Convert to JSON
            json_output = json.dumps(sensor_data, indent=2)
            
            # Display results
            print(f"\n📊 Sensor Readings - {time.strftime('%Y-%m-%d %H:%M:%S')}")
            
            # DHT11 results
            dht_status = sensor_data['dht11']['status']
            if dht_status == "OK":
                print(f"✅ DHT11: {sensor_data['dht11']['temperature_c']}°C, " 
                      f"{sensor_data['dht11']['humidity']}% RH")
            else:
                print(f"❌ DHT11: {dht_status}")
            
            # DS18B20 results
            for sensor_id, data in sensor_data['ds18b20'].items():
                if data['status'] == "OK":
                    print(f"✅ {sensor_id}: {data['temperature_c']}°C")
                else:
                    print(f"❌ {sensor_id}: {data['status']}")
            
            # Full JSON output
            print("\n📦 JSON Payload:")
            print(json_output)
            print("-" * 50)
            
            # Wait between readings
            time.sleep(5.0)

    except KeyboardInterrupt:
        print("\n🛑 Script stopped by user.")
        # Clean up
        dhtDevice.exit()
        print("Sensor connections cleaned up.")
