import Simalted_GPIO as pigpio

import time

pi = pigpio.pi()

# Define GPIO pins
GPIO1 = 17
GPIO2 = 27

# Set GPIOs as inputs with pull-down resistors
pi.set_mode(GPIO1, pigpio.INPUT)
pi.set_mode(GPIO2, pigpio.INPUT)
pi.set_pull_up_down(GPIO1, pigpio.PUD_DOWN)
pi.set_pull_up_down(GPIO2, pigpio.PUD_DOWN)


# Callback function
def callback(gpio, level, tick):

    if pi.read(GPIO1) and pi.read(GPIO2):
        print(f"Both GPIOs triggered at {tick}")
    else:
        print(f"GPIO {gpio} triggered at {tick}; {level}")


# Attach callbacks
pi.callback(GPIO1, pigpio.RISING_EDGE, callback)
pi.callback(GPIO2, pigpio.RISING_EDGE, callback)

# Simulate GPIO signals (trigger both at the same time)
time.sleep(1)
print("Simulating GPIO triggers...")
pi.gpio_trigger(GPIO1, 10)
pi.gpio_trigger(GPIO2)
time.sleep(0.01)  # Short delay to ensure both are detected
# pi.write(GPIO1, 0)
# pi.write(GPIO2, 0)

# Keep the script running to catch events
time.sleep(2)

# Cleanup
pi.stop()


if __name__ == "__main__":
    pass
