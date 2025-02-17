# screen_switcher.py

from kivy.uix.screenmanager import ScreenManager, Screen
from itertools import cycle
from kivy.core.window import Window
from kivy.clock import Clock


class CustomScreenSwitcher(ScreenManager):
    def __init__(self, **kwargs):
        super(CustomScreenSwitcher, self).__init__(**kwargs)
        self.list_of_screens = []
        self.cycle_screen = None
        Window.bind(on_key_down=self.on_key_down)

        self.clock_event = None

    def on_current_screen(self, *args):
        # Cancel any existing clock event before starting a new one
        if self.clock_event:
            self.clock_event.cancel()

        # Start a new clock event that updates the currently active screen
        self.clock_event = Clock.schedule_interval(self.update_active_screen, 1)
      #  self.change_screen = Clock.schedule_interval(self.debugchange, 5) use is no keyboard is avaliable for raspbeery

    def update_active_screen(self, dt):
        # Call a `refresh` method on the active screen, if it exists

        self.current_screen.refresh()

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


    # use if no keyboard is avalible
   # def debugchange(self, window, *args, **kwargs):
   #     self.switch_to_next()




