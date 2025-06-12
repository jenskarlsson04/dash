
import os
os.environ["KIVY_NO_CONSOLELOG"] = "1"
os.environ["KIVY_NO_FILELOG"] = "1"
os.environ["KIVY_LOG_LEVEL"] = "error"
os.environ["KIVY_AUDIO"] = "dummy"


# rest of your imports

from kivy.config import Config

# Config.set('graphics', 'fullscreen', 1)
Config.set("graphics", "width", 1024)
Config.set("graphics", "height", 600)
Config.set("graphics", "dpi", "96")  # Adjust as needed
Config.set("graphics", "show_cursor", 0)

from kivy.app import App
from gui.pages.Dash2 import Dash2
from gui.pages.Faults import Faults
from gui.pages.Afterdrive import Afterdrive
from gui.pages.Inverter import Inverter
from gui.pages.TSAC import TSAC
from gui.screen_switcher.screen_switcher import (
    CustomScreenSwitcher,
)  # Renamed to CentralizedScreenSwitcher


class MainApp(App):
    def build(self):
        # Use CentralizedScreenSwitcher instead of the default CustomScreenSwitcher
        sm = CustomScreenSwitcher()

        # Add screens to the screen manager
        sm.add_screen(Dash2(name="dashboard2"))
        sm.add_screen(TSAC(name="tsac"))
        sm.add_screen(Inverter(name="inverter"))
        sm.add_screen(Faults(name="faults"))
        sm.add_screen(Afterdrive(name="afterdrive"))

        # Bind to detect screen changes and reset the clock update
        sm.bind(current=sm.on_current_screen)

        # set the first screen to activ, BUG: if removed needs two presses to switch screen,
        # how does it add the first screen?
        sm.switch_to_next()

        return sm


if __name__ == "__main__":
    MainApp().run()
