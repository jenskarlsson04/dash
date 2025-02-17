import os

os.environ["KIVY_NO_FILELOG"] = "1"  # eliminate file log
from kivy.config import Config


Config.set("graphics", "width", "1024")
Config.set("graphics", "height", "600")
Config.set("graphics", "dpi", "96")

from kivy.app import App
from pages.Dash import Dash
from pages.Inverter import Inverter
from pages.Orion import Orion
from pages.TSCU import TSCU
from screen_switcher.screen_switcher import (
    CustomScreenSwitcher,
)  # Renamed to CentralizedScreenSwitcher


class MainApp(App):
    def build(self):
        # Use CentralizedScreenSwitcher instead of the default CustomScreenSwitcher
        sm = CustomScreenSwitcher()

        # Add screens to the screen manager
        # sm.add_screen(Inverter(name="inverter"))
        # sm.add_screen(Dash(name="Dashboard"))
        # sm.add_screen(Orion(name="orion"))
        sm.add_screen(TSCU(name="tscu"))

        # Bind to detect screen changes and reset the clock update
        sm.bind(current=sm.on_current_screen)

        return sm


if __name__ == "__main__":
    MainApp().run()
