#!/usr/bin/env python3

import board
import adafruit_dht
import time

# --- Configuration ---
# Your specified Data Pin (Physical Pin 7) corresponds to BCM GPIO 4
DHT_PIN = board.D4

# Initialize the DHT11 device using the correct pin
# Use adafruit_dht.DHT22 for DHT22 sensors
dhtDevice = adafruit_dht.DHT11(DHT_PIN)

print(f"--- DHT11 Reader Initialized (Data Pin: BCM {DHT_PIN.id}) ---")

try:
    while True:
        try:
            # Read the sensor data
            temperature_c = dhtDevice.temperature
            humidity = dhtDevice.humidity

            # Check if readings are valid (sometimes the first reading fails)
            if temperature_c is not None and humidity is not None:
                # Convert Celsius to Fahrenheit
                temperature_f = temperature_c * (9 / 5) + 32

                print("-" * 30)
                print(f"✅ Temperature: {temperature_c:.1f}°C / {temperature_f:.1f}°F")
                print(f"✅ Humidity:    {humidity:.1f}%")
                print("-" * 30)
            else:
                print("❌ Failed to retrieve data from DHT11 sensor. Retrying...")

        # Catch a common error that occurs with DHT sensors (requires retrying)
        except RuntimeError as error:
            # Errors happen, but most are "Checksum failed" and safe to ignore/retry
            print(f"⚠️ Runtime Error: {error.args[0]}")
            time.sleep(2.0) # Wait a bit before trying again
            continue

        # Wait 5 seconds between readings
        time.sleep(5.0)

# Allow the script to be stopped cleanly with Ctrl+C
except KeyboardInterrupt:
    print("\nScript stopped by user.")
    dhtDevice.exit() # Clean up the sensor connection