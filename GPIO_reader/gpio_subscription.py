from dataclasses import dataclass
import Simalted_GPIO as pigpio


@dataclass
class GPIO_PIN:
    pin: int



class GIPOConfiguration:

    _instance = None  # Store the single instance

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):

        self.pi = pigpio.pi()

        self.btn_lap = GPIO_PIN(22)
        self.btn_screen = GPIO_PIN(27)


        self.__init_gpio_input(self.btn_lap, self.btn_screen)

    def __init_gpio_input(self, *args: GPIO_PIN):
        for gpio in args:
            self.pi.set_mode(gpio.pin, pigpio.INPUT)

    def __init_gpio_output(self, *args: GPIO_PIN):
        pass




listeners = {}

#callback(puls_length)

def subscribe_gpio_pint(gpio: GPIO_PIN, callback):
    """
    Subscribe a GPIO.
    """
    if gpio.pin in listeners:
        listeners[gpio.pin].append(callback)
    else:
        listeners[gpio.pin] = [callback]


def publish_message(gpio_pin: int, puls_length: int):
    """
    Publish on a GPIO pin.
    """
    if gpio_pin in listeners:
        for callback in listeners[gpio_pin]:
            callback(puls_length)


if __name__ == '__main__':
    pass