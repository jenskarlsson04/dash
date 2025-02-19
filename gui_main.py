import os

os.environ["KIVY_NO_FILELOG"] = "1"  # eliminate file log
from kivy.config import Config
from pages.Dash2 import Dash2
from pages.Inverter import Inverter
from pages.TSAC import TSAC
from pages.Dash import Dash
Config.set("graphics", "width", "1024")
Config.set("graphics", "height", "600")
Config.set("graphics", "dpi", "96")

from kivy.app import App
from screen_switcher.screen_switcher import (
    CustomScreenSwitcher,
)  # Renamed to CentralizedScreenSwitcher


class MainApp(App):
    def build(self):
        # Use CentralizedScreenSwitcher instead of the default CustomScreenSwitcher
        sm = CustomScreenSwitcher()

        # Add screens to the screen manager
        #sm.add_screen(Dash2(name="dashboard2"))
        #sm.add_screen(Inverter(name="inverter"))
        #sm.add_screen(Dash(name="Dashboard"))
        # sm.add_screen(Orion(name="orion"))
        sm.add_screen(TSAC(name="tsac"))

        # Bind to detect screen changes and reset the clock update
        sm.bind(current=sm.on_current_screen)

        return sm


if __name__ == "__main__":
    MainApp().run()
