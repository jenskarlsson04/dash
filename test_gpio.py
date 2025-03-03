from GPIO_reader import subscribe_gpio_pint, btn_screen
import pigpio

pin = 16

def run(gpio, level, tick):

    print("GPIO triggered")

pi = pigpio.pi()

"""
Configure pigpio
"""
# Set gpio as pull-down resistors
pi.set_mode(pin, pigpio.PUD_UP)

# Attach callbacks rising edge
pi.callback(pin, pigpio.RISING_EDGE, run)

# falling edge
pi.callback(pin, pigpio.FALLING_EDGE, run)



#subscribe_gpio_pint(btn_screen, run)


if __name__ == "__main__":
    while True:
        pass
