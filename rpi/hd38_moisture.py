#!/usr/bin/env python3

# pip install adafruit-circuitpython-typing digitalio

import time
import json
import traceback 
# Import Pin and DigitalInOut for basic digital reading
from adafruit_blinka.microcontroller.bcm283x.pin import Pin
from digitalio import DigitalInOut, Direction, Pull

# --- Configuration ---
# NOTE: The HD-38 is a digital sensor, usually connected to a Digital GPIO pin.
# We will use BCM GPIO pin 4 (Physical Pin 7) for consistency, but you MUST 
# ensure your sensor is wired to this pin.
HD38_PIN_NUM = 4 
HD38_PIN = Pin(HD38_PIN_NUM)
SENSOR_ID = "RPI_SENSOR_1_HD38" # Unique ID for this device

# Initialize the Digital Input Pin
# The HD-38 sensor module typically outputs LOW when the threshold is met (e.g., WET)
# and HIGH when it is not (e.g., DRY). We configure the pin as an input.
try:
    sensor_pin = DigitalInOut(HD38_PIN)
    sensor_pin.direction = Direction.INPUT
    # The HD-38 usually has an internal pull-up/down but specifying PULL_UP can help stability
    sensor_pin.pull = Pull.UP 
except Exception as e:
    print(f"FATAL ERROR: Could not initialize HD-38 pin (BCM {HD38_PIN_NUM}).")
    print(f"Error: {e}")
    # Exit if pin cannot be initialized
    exit(1)


def get_hd38_data():
    """Reads HD-38 digital status and returns data as a dictionary."""
    data = {}
    
    try:
        # Read the digital value from the pin
        # value is True (HIGH) or False (LOW)
        pin_value = sensor_pin.value

        # The HD-38 typically outputs LOW (False) when the condition is met (e.g., WET/TRIGGERED)
        # and HIGH (True) when the condition is NOT met.
        
        # We define the status based on the typical LOW-means-triggered behavior
        if pin_value is False:
            # Pin is LOW (0V) -> Condition Met (e.g., WET, or threshold reached)
            status_text = "TRIGGERED" # or "WET" if it's moisture
        else:
            # Pin is HIGH (3.3V) -> Condition Not Met (e.g., DRY, or threshold not reached)
            status_text = "NORMAL" # or "DRY"
        
        # Data is valid, construct the dictionary
        data = {
            "id": SENSOR_ID,
            "timestamp": time.time(),
            "pin_value_raw": pin_value, # True/False
            "status_digital": status_text,
            "status": "OK"
        }

    except Exception as e:
        # Catch any unexpected errors
        print(f"⚠️ Unexpected Error during read: {e}")
        traceback.print_exc()
        data = {
            "id": SENSOR_ID,
            "timestamp": time.time(),
            "status": "UNEXPECTED_ERROR",
            "message": str(e)
        }
        
    return data

if __name__ == '__main__':
    print(f"--- HD-38 Digital Reader Initialized (Data Pin: BCM {HD38_PIN_NUM}) ---")
    
    try:
        while True:
            sensor_data_dict = get_hd38_data()
            
            # Convert the Python dictionary to a JSON string
            json_output = json.dumps(sensor_data_dict)
            
            # Print the result
            print("-" * 50)
            if sensor_data_dict.get("status") == "OK":
                print(f"✅ JSON Payload Ready: {json_output}")
            else:
                print(f"❌ Error Payload: {json_output}")

            # Wait 1 second between readings (digital sensors can be read faster)
            time.sleep(1.0)

    except KeyboardInterrupt:
        print("\nScript stopped by user.")
        # No specific sensor cleanup needed for DigitalInOut, but good practice to release the pin
        sensor_pin.direction = Direction.INPUT # Safety reset
        sensor_pin.close()