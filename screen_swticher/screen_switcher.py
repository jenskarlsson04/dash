# screen_switcher.py

from kivy.uix.screenmanager import ScreenManager, Screen
from itertools import cycle
from kivy.core.window import Window

class CustomScreenSwitcher(ScreenManager):
    def __init__(self, **kwargs):
        super(CustomScreenSwitcher, self).__init__(**kwargs)
        self.list_of_screens = []
        self.cycle_screen = None
        Window.bind(on_key_down=self.on_key_down)

    def add_screen(self, widget: Screen):
        self.list_of_screens.append(widget)
        self.add_widget(widget)
        self.cycle_screen = cycle(self.list_of_screens)

    def switch_to_next(self):
        # Stop the clock on the current screen before switching
        if hasattr(self.current_screen, "on_pre_leave"):
            self.current_screen.on_pre_leave()

        # Switch to the next screen
        next_screen = next(self.cycle_screen)
        self.current = next_screen.name

        # Start the clock on the newly active screen
        if hasattr(self.current_screen, "on_pre_enter"):
            self.current_screen.on_pre_enter()

    def on_key_down(self, window, key, *args):
        if key == ord('k'):
            self.switch_to_next()
