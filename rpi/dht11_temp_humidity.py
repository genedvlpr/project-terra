#!/usr/bin/env python3

import adafruit_blinka as board
import adafruit_dht
import time
import json
import traceback # Useful for better error logging

# --- Configuration ---
# Your specified Data Pin (Physical Pin 7) corresponds to BCM GPIO 4
DHT_PIN = board.D4 
SENSOR_ID = "RPI_SENSOR_1" # Unique ID for this device

# Initialize the DHT11 device
dhtDevice = adafruit_dht.DHT11(DHT_PIN)

def get_dht11_data():
    """Reads DHT11 sensor and returns data as a dictionary."""
    data = {}
    
    try:
        # Read the sensor data
        temperature_c = dhtDevice.temperature
        humidity = dhtDevice.humidity

        # Check if readings are valid
        if temperature_c is not None and humidity is not None:
            # Data is valid, construct the dictionary
            data = {
                "id": SENSOR_ID,
                "timestamp": time.time(),
                "temperature_c": round(temperature_c, 1),
                "temperature_f": round(temperature_c * (9 / 5) + 32, 1),
                "humidity": round(humidity, 1),
                "status": "OK"
            }
        else:
            # Data read failed (often a checksum error)
            data = {
                "id": SENSOR_ID,
                "timestamp": time.time(),
                "status": "READ_FAILED"
            }

    except RuntimeError as error:
        # Specific hardware timing error (safe to ignore and retry)
        data = {
            "id": SENSOR_ID,
            "timestamp": time.time(),
            "status": "RUNTIME_ERROR",
            "message": str(error)
        }
    except Exception as e:
        # Catch any other unexpected errors
        print(f"⚠️ Unexpected Error: {e}")
        traceback.print_exc()
        data = {
            "id": SENSOR_ID,
            "timestamp": time.time(),
            "status": "UNEXPECTED_ERROR",
            "message": str(e)
        }
        
    return data

if __name__ == '__main__':
    print(f"--- DHT11 Reader Initialized (Data Pin: BCM {DHT_PIN.id}) ---")
    
    try:
        while True:
            sensor_data_dict = get_dht11_data()
            
            # Convert the Python dictionary to a JSON string
            json_output = json.dumps(sensor_data_dict)
            
            # Print the result (In the final app, this JSON string will be sent via Bluetooth)
            print("-" * 50)
            if sensor_data_dict.get("status") == "OK":
                print(f"✅ JSON Payload Ready: {json_output}")
            else:
                print(f"❌ Error Payload: {json_output}")

            # Wait 5 seconds between readings
            time.sleep(5.0)

    except KeyboardInterrupt:
        print("\nScript stopped by user.")
        # Clean up the sensor connection
        if 'dhtDevice' in locals() or 'dhtDevice' in globals():
            dhtDevice.exit()