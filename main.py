# main.py
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from Pages.DriverDashboard import DriverDashboard
from kivy.config import Config

# Config windows size

Config.set("graphics", "width", "1024")
Config.set("graphics", "height", "600")
Config.write()

class MainScreen(Screen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        # Create an instance of SpeedPage and add it to the screen
        self.DriverDash = DriverDashboard()
        self.add_widget(self.DriverDash)


class DriverDash(App):
    def build(self):
        # Create a ScreenManager and add the MainScreen
        sm = ScreenManager()
        sm.add_widget(MainScreen(name='main'))
        return sm

if __name__ == '__main__':
    DriverDash().run()
