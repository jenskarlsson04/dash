import time
from GPIO_reader.gpio_subscription import publish_message
from GPIO_reader.GPIO_datamodel import GPIO_PIN

GPIO_DEBUG = False

try:
    import pigpio
except ImportError:
    GPIO_DEBUG = False
    from GPIO_reader.keyboard_gpio import KeyboardGpio
    print("WARNING: DEBUG MODE ON. Use keyboard to simulate gpio")


btn_lap = GPIO_PIN(6)
btn_screen = GPIO_PIN(13)
btn_reset = GPIO_PIN(19)
btn_idk = GPIO_PIN(5)


class GIPOConfiguration:
    """
    class to handle GPIO pins and the interrupts
    """

    _instance = None  # Store the single instance

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):

        self.pi = pigpio.pi()

        self.btn_lap = btn_lap
        self.btn_screen = btn_screen
        self.btn_reset = btn_reset
        self.btn_idk = btn_idk

        self.time_button_press_down = {}

        """
        Configure pigpio
        """
        # Set gpio as pull-down resistors
        self.pi.set_mode(self.btn_lap.pin, pigpio.INPUT)
        self.pi.set_mode(self.btn_screen.pin, pigpio.INPUT)
        self.pi.set_mode(self.btn_reset.pin, pigpio.INPUT)
        self.pi.set_mode(self.btn_idk.pin, pigpio.INPUT)

        self.pi.set_pull_up_down(self.btn_lap.pin, pigpio.PUD_UP)
        self.pi.set_pull_up_down(self.btn_screen.pin, pigpio.PUD_UP)
        self.pi.set_pull_up_down(self.btn_reset.pin, pigpio.PUD_UP)
        self.pi.set_pull_up_down(self.btn_idk.pin, pigpio.PUD_UP)

        self.pi.set_mode(self.btn_reset.pin, pigpio.INPUT)

        # Attach callbacks
        self.pi.callback(
            self.btn_lap.pin, pigpio.EITHER_EDGE, self.__callback_handle_gpio_event
        )
        self.pi.callback(
            self.btn_screen.pin, pigpio.EITHER_EDGE, self.__callback_handle_gpio_event
        )

    """
    Funcs to handle GPIO pins and the interrupts and to calculate the time between
    """

    def __handle_press_down(self, pin: int):
        if self.pi.read(pin) == 0:  # Ensure pin is truly low
            self.time_button_press_down[pin] = time.time()

    def __handle_press_up(self, pin: int):
        if pin in self.time_button_press_down:
            start_time = self.time_button_press_down.get(pin)

            end_time = time.time()

            duration = end_time - start_time

            publish_message(pin, duration)

    def __callback_handle_gpio_event(self, gpio, level, tick):
        """
        Handle GPIO edge events; only trigger press up if there was a press down.
        """
        if level == 1 and gpio in self.time_button_press_down:
            self.__handle_press_up(gpio)
        elif level == 0:
            self.__handle_press_down(gpio)

if not GPIO_DEBUG:
    gpio = GIPOConfiguration()
else:
    gpio = KeyboardGpio()

if __name__ == "__main__":

    gpio = GIPOConfiguration()
