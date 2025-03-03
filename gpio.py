import RPi.GPIO as GPIO
import time

# List of all GPIO pins (BCM mode)
GPIO_PINS = [2, 3, 4, 17, 27, 22, 10, 9, 11, 5, 6, 13, 19, 26, 14, 15, 18, 23, 24, 25, 8, 7, 12, 16, 20, 21]

# Setup
GPIO.setmode(GPIO.BCM)  # Use BCM numbering

# Configure all pins as input with pull-down resistors
for pin in GPIO_PINS:
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

print("Scanning GPIO states (Press Ctrl+C to exit)...")

try:
    while True:
        print("\nGPIO Status:")
        for pin in GPIO_PINS:
            state = "HIGH" if GPIO.input(pin) else "LOW"
            print(f"GPIO {pin}: {state}")
        time.sleep(1)  # Scan every 1 second
except KeyboardInterrupt:
    print("\nExiting...")
finally:
    GPIO.cleanup()
