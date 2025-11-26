import RPi.GPIO as GPIO
import time

# --- Configuration ---
# Use BCM (Broadcom SOC channel) numbering for GPIO pin reference.
# We are using GPIO 17 (Physical Pin 11) for the sensor's Digital Out (DO)
OBSTACLE_PIN = 17

def setup():
    """Initializes the GPIO settings."""
    # Set the numbering mode to BCM
    GPIO.setmode(GPIO.BCM)
    
    # Set the obstacle pin as an INPUT pin
    # The pull-up/pull-down resistor is often not needed as the HD-38 module
    # has a built-in pull-up resistor (due to the comparator logic).
    GPIO.setup(OBSTACLE_PIN, GPIO.IN) 
    
    print("GPIO setup complete. Waiting for sensor readings...")

def loop():
    """Continuously monitors the sensor state."""
    try:
        while True:
            # Read the state of the Digital Output (DO) pin.
            # On most HD-38 modules:
            # - LOW (0) means OBSTACLE DETECTED (IR light reflected back)
            # - HIGH (1) means NO OBSTACLE (or light not reflected)
            
            sensor_state = GPIO.input(OBSTACLE_PIN)
            
            if sensor_state == GPIO.LOW:
                print(">>> OBSTACLE DETECTED! <<<")
            else:
                print("--- Clear Path ---")
            
            # Wait for a short period before checking again
            time.sleep(0.5)

    except KeyboardInterrupt:
        # Gracefully exit the program when Ctrl+C is pressed
        print("\nProgram stopped by user.")
        GPIO.cleanup() # Clean up all GPIO settings

def main():
    """Main function to run the setup and loop."""
    setup()
    loop()

if __name__ == '__main__':
    main()
