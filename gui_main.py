import os

from gui.pages.Afterdrive import Afterdrive

os.environ['KIVY_NO_FILELOG'] = '1'  # eliminate file log
from kivy.config import Config
#Config.set('graphics', 'fullscreen', 1)
Config.set('graphics', 'width', 1024)
Config.set('graphics', 'height', 600)
Config.set('graphics', 'dpi', '96')  # Adjust as needed

from kivy.app import App
from gui.pages.Dash import Dash
from gui.pages.Dash2 import Dash2
from gui.pages.Faults import Faults
from gui.pages.Afterdrive import Afterdrive
from gui.pages.Inverter import Inverter
from gui.pages.TSAC import TSAC
from gui.screen_switcher.screen_switcher import CustomScreenSwitcher  # Renamed to CentralizedScreenSwitcher


class MainApp(App):
    def build(self):
        # Use CentralizedScreenSwitcher instead of the default CustomScreenSwitcher
        sm = CustomScreenSwitcher()

        # Add screens to the screen manager
        sm.add_screen(Afterdrive(name="afterdrive"))

        sm.add_screen(Dash2(name="dashboard2"))
        sm.add_screen(Faults(name="faults"))
        sm.add_screen(TSAC(name="tsac"))
        sm.add_screen(Inverter(name="inverter"))
        sm.add_screen(Dash(name="Dashboard"))

        # Bind to detect screen changes and reset the clock update
        sm.bind(current=sm.on_current_screen)

        return sm


if __name__ == "__main__":
    MainApp().run()
