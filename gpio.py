import RPi.GPIO as GPIO
import time

# GPIO pin number where the button is connected
BUTTON_PIN = 6

# Setup
GPIO.setmode(GPIO.BCM)  # Use BCM pin numbering
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Enable internal pull-up resistor

print("Press the button to test...")

try:
    while True:
        if GPIO.input(BUTTON_PIN) == GPIO.LOW:  # Button is pressed
            print("Button Pressed!")
            time.sleep(0.2)  # Debounce delay
except KeyboardInterrupt:
    print("\nExiting...")
finally:
    GPIO.cleanup()  # Cleanup GPIO on exit
