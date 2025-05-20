from kivy.core.window import Window
from GPIO_reader.gpio_subscription import publish_message
import time

class KeyboardGpio:
    def __init__(self):

        # List to bind a key to a virtual gpio pin
        self.bind_keys = {
            "k": 13,
            "o": 27,
            "l": 22,
        }

        self.handle_press_down = {}

        Window.bind(on_key_down=self.on_key_down, on_key_up=self.on_key_up)
        pass


    def on_key_down(self, window, key, *args):
        # Keyboard events occur on the main thread.
        letter = chr(key)

        if letter in self.bind_keys:
            if letter not in self.handle_press_down or self.handle_press_down[letter] is None:
                print("key down")
                print(time.time())
                self.handle_press_down[letter] = time.time()

    def on_key_up(self, window, key, *args):

        print("key up")
        letter = chr(key)

        if letter in self.bind_keys:
            start_time = self.handle_press_down.get(letter)

            self.handle_press_down[letter] = None

            end_time = time.time()

            duration = end_time - start_time

            publish_message(self.bind_keys[letter], duration)



if __name__ == "__main__":
    from kivy.app import App
    from GPIO_reader.gpio_subscription import subscribe_gpio_pint
    from GPIO_reader.gpio_class import btn_screen

    def handle_screen_switch(puls_length):
        print(f"K pressed with delay {puls_length}")

    subscribe_gpio_pint(btn_screen, handle_screen_switch)

    keyboard = KeyboardGpio()

    class TestApp(App):
        def build(self):
            return

    TestApp().run()
    print(ord("k"))