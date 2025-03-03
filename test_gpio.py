import pigpio
import time

# GPIO pin to monitor
GPIO_PIN = 16  # Change this to the GPIO number you want to test

# Initialize pigpio
pi = pigpio.pi()

if not pi.connected:
    print("Error: pigpio daemon is not running!")
    exit(1)

# Configure GPIO as input with pull-up resistor
pi.set_mode(GPIO_PIN, pigpio.INPUT)
pi.set_pull_up_down(GPIO_PIN, pigpio.PUD_DOWN)  # Use pull-up for button input

# Callback function to execute when the GPIO state changes
def gpio_callback(gpio, level, tick):
    state = "HIGH" if level else "LOW"
    print(f"GPIO {gpio} changed to {state} at tick {tick}")

# Set up callback to detect changes
cb = pi.callback(GPIO_PIN, pigpio.EITHER_EDGE, gpio_callback)

print(f"Monitoring GPIO {GPIO_PIN}... Press Ctrl+C to exit.")

try:
    while True:
        time.sleep(1)  # Keep script running
except KeyboardInterrupt:
    print("\nExiting...")
finally:
    cb.cancel()  # Stop the callback
    pi.stop()  # Cleanup pigpio resources
