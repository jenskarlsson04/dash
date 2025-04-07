from kivy.uix.screenmanager import ScreenManager, Screen
from itertools import cycle
from kivy.core.window import Window
from kivy.clock import Clock
from GPIO_reader import subscribe_gpio_pint, btn_screen


class CustomScreenSwitcher(ScreenManager):
    def __init__(self, **kwargs):
        super(CustomScreenSwitcher, self).__init__(**kwargs)
        self.list_of_screens = []
        self.cycle_screen = None
        Window.bind(on_key_down=self.on_key_down)

        self.clock_event = None

        # Use the thread-safe version for the GPIO callback.
        subscribe_gpio_pint(btn_screen, self.switch_to_next)

    def on_current_screen(self, *args):
        # Cancel any existing clock event before starting a new one
        if self.clock_event:
            self.clock_event.cancel()

        # Start a new clock event that updates the currently active screen
        self.clock_event = Clock.schedule_interval(self.update_active_screen, 0.0167)

    def update_active_screen(self, dt):
        # Call a `refresh` method on the active screen, if it exists.
        if hasattr(self.current_screen, "refresh"):
            self.current_screen.refresh()

    def add_screen(self, widget: Screen):
        self.list_of_screens.append(widget)
        self.add_widget(widget)
        self.cycle_screen = cycle(self.list_of_screens)

    def switch_to_next(self, time=None):
        # Stoppa klockan på den aktuella skärmen innan byte.
        if hasattr(self.current_screen, "on_pre_leave"):
            self.current_screen.on_pre_leave()

        # Byt till nästa skärm.
        next_screen = next(self.cycle_screen)
        self.current = next_screen.name

        # Starta klockan på den nya skärmen.
        if hasattr(self.current_screen, "on_pre_enter"):
            self.current_screen.on_pre_enter()

    def on_key_down(self, window, key, *args):
        # Keyboard events occur on the main thread.
        if key == ord("k"):
            self.switch_to_next()
