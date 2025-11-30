import serial
import time

# --- YOU MUST CALIBRATE THESE VALUES ---
# Change these values to YOUR sensor's readings (e.g., in air vs. in water)
DRY_VALUE = 600   # Raw value when the sensor is in the air (0% moisture)
WET_VALUE = 250   # Raw value when the sensor is submerged in water (100% moisture)

# --- YOUR PORT NAME ---
# Change this to what you found in Step 2.2 (e.g., '/dev/ttyACM0')
PORT_NAME = '/dev/ttyUSB0' 
BAUD_RATE = 9600 

print(f"Attempting to connect to Arduino on {PORT_NAME}...")

try:
    ser = serial.Serial(PORT_NAME, BAUD_RATE, timeout=1)
    ser.flush()
    print("Connection established. Reading data...")
    
    while True:
        if ser.in_waiting > 0:
            # Read the incoming line (the raw number from Arduino)
            line = ser.readline().decode('utf-8').rstrip()
            
            if line.isdigit():
                raw_value = int(line)
                
                # Formula to map the raw value to a percentage (0-100)
                moisture_percentage = int(((DRY_VALUE - raw_value) / (DRY_VALUE - WET_VALUE)) * 100)
                moisture_percentage = max(0, min(100, moisture_percentage))

                # Output
                print(f"RAW: {raw_value} | Moisture: {moisture_percentage}%", end='\r') 
        
        time.sleep(0.5)

except serial.SerialException as e:
    print(f"\n ERROR: Could not open serial port {PORT_NAME}. Check cable and port name.")
except KeyboardInterrupt:
    print("\nScript terminated by user.")
except Exception as e:
    print(f"\nAn unexpected error occurred: {e}")
finally:
    if 'ser' in locals() and ser.is_open:
        ser.close() 
