from dataclasses import dataclass
import time
from GPIO_reader.gpio_subscription import publish_message
from GPIO_reader import btn_lap, btn_screen

GPIO_DEBUG = False

if GPIO_DEBUG:
    import GPIO_reader.Simalted_GPIO as pigpio
else:
    import pigpio

def set_debug():
    global GPIO_DEBUG
    GPIO_DEBUG = True

@dataclass
class GPIO_PIN:
    pin: int



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

        self.time_button_press_down = {}

        """
        Configure pigpio
        """
        #Set gpio as pull-down resistors
        self.pi.set_mode(self.btn_lap.pin, pigpio.PUD_DOWN)
        self.pi.set_mode(self.btn_screen.pin, pigpio.PUD_DOWN)

        #Attach callbacks rising edge
        self.pi.callback(self.btn_lap.pin, pigpio.RISING_EDGE, self.__callback_handle_gpio_event)
        self.pi.callback(self.btn_screen.pin, pigpio.RISING_EDGE, self.__callback_handle_gpio_event)

        # falling edge
        self.pi.callback(self.btn_lap.pin, pigpio.FALLING_EDGE, self.__callback_handle_gpio_event)
        self.pi.callback(self.btn_screen.pin, pigpio.FALLING_EDGE, self.__callback_handle_gpio_event)





    """
    Funcs to handle GPIO pins and the interrupts and to calculate the time between
    """
    def __handle_press_down(self, pin: int):

        self.time_button_press_down[pin] = time.time()

    def __handle_press_up(self, pin: int):

        start_time = self.time_button_press_down[pin]

        end_time = time.time()

        duration = end_time - start_time

        publish_message(pin, duration)

    def __callback_handle_gpio_event(self, gpio, level, tick):
        """
        Change place on press down and upp if pull up or pull down
        """
        if level == 1:
            self.__handle_press_down(gpio)
        else:
            self.__handle_press_up(gpio)

gpio = GIPOConfiguration()

if __name__ == "__main__":

    gpio = GIPOConfiguration()

