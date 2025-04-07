import pigpio
import time

# List of GPIO pins to scan (BCM numbering)
GPIO_PINS = [
    2,
    3,
    4,
    17,
    27,
    22,
    10,
    9,
    11,
    5,
    6,
    13,
    19,
    26,
    14,
    15,
    18,
    23,
    24,
    25,
    8,
    7,
    12,
    16,
    20,
    21,
]

# Initialize pigpio
pi = pigpio.pi()

if not pi.connected:
    print("Error: pigpio daemon is not running!")
    exit(1)

# Configure all pins as input with pull-down resistors
for pin in GPIO_PINS:
    pi.set_mode(pin, pigpio.INPUT)
    pi.set_pull_up_down(pin, pigpio.PUD_DOWN)  # Use pull-down to default to LOW

print("Scanning GPIO states (Press Ctrl+C to exit)...")

try:
    while True:
        print("\nGPIO Status:")
        for pin in GPIO_PINS:
            if pi.read(pin):
                print(f"GPIO {pin}")
        time.sleep(1)  # Scan every 1 second
except KeyboardInterrupt:
    print("\nExiting...")
finally:
    pi.stop()  #
