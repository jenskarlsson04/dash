from GPIO_reader.GPIO_datamodel import GPIO_PIN
from kivy.clock import mainthread


listeners = {}

# callback(puls_length)


def subscribe_gpio_pint(gpio: GPIO_PIN, callback):
    """
    Subscribe a GPIO.
    """
    if gpio.pin in listeners:
        listeners[gpio.pin].append(callback)
    else:
        listeners[gpio.pin] = [callback]


@mainthread
def publish_message(gpio_pin: int, puls_length: int):
    """
    Publish on a GPIO pin.
    """
    if gpio_pin in listeners:
        for callback in listeners[gpio_pin]:
            callback(puls_length)


if __name__ == "__main__":
    pass
