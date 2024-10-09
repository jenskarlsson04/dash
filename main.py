# main.py
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen

from Pages.Debug import Debug
from Pages.DriverDashboard import DriverDashboard
import Pages.pageselector as page_selector

class MainScreen(Screen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        # Create an instance of SpeedPage and add it to the screen
        self.DriverDash = DriverDashboard()
        self.add_widget(self.DriverDash)

class DebugScreen(Screen):
    def __init__(self, **kwargs):
        super(DebugScreen, self).__init__(**kwargs)
        self.Debug = Debug()
        self.add_widget(self.Debug)
    pass


class DriverDash(App):
    def build(self):
        # Create a ScreenManager and add the MainScreen
        sm = ScreenManager()
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(DebugScreen(name='debug'))
        page_selector.set_screen_manager(sm)
        page_selector.bind_keyboard()
        return sm

if __name__ == '__main__':
    DriverDash().run()
