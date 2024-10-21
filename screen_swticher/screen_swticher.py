from kivy.uix.screenmanager import ScreenManager, Screen
from itertools import cycle


class CustomScreenSwitcher(ScreenManager):
    def __init__(self, **kwargs):
        super(CustomScreenSwitcher, self).__init__(**kwargs)
        self.current = None
        self.list_of_screen_names = []
        self.cycle_screen = cycle(self.list_of_screen_names)

    def add_screen(self, widget: Screen):
        self.list_of_screen_names.append(widget)
        self.add_widget(widget)

        self.cycle_screen = cycle(self.list_of_screen_names)

    def switch_to_next(self):
        self.current = next(self.cycle_screen).name
