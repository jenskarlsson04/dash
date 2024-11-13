from kivy.uix.screenmanager import ScreenManager, Screen
from itertools import cycle
from pages.screen_interface import ScreenInterface
from kivy.clock import Clock


class CustomScreenSwitcher(ScreenManager):
    def __init__(self, **kwargs):
        super(CustomScreenSwitcher, self).__init__(**kwargs)
        self.current = None
        self.list_of_screen_names = []
        self.cycle_screen = cycle(self.list_of_screen_names)
        Clock.schedule_interval(self.cycle_screen, 0.5)

    def add_screen(self, widget: ScreenInterface):
        widget.add_screen_switcher(self.switch_to_next)
        self.list_of_screen_names.append(widget)
        self.add_widget(widget)

        self.cycle_screen = cycle(self.list_of_screen_names)

    def switch_to_next(self):
        self.current = next(self.cycle_screen).name


