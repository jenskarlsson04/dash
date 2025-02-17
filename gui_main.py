import os
os.environ['KIVY_NO_FILELOG'] = '1'  # eliminate file log
from kivy.app import App
from gui.pages.Dash import Dash
from gui.pages.Inverter import Inverter
from gui.pages.Orion import Orion
from gui.pages.TSCU import TSCU
from gui.screen_switcher.screen_switcher import CustomScreenSwitcher  # Renamed to CentralizedScreenSwitcher


class MainApp(App):
    def build(self):
        # Use CentralizedScreenSwitcher instead of the default CustomScreenSwitcher
        sm = CustomScreenSwitcher()

        # Add screens to the screen manager
        sm.add_screen(Inverter(name="inverter"))
        sm.add_screen(Dash(name="Dashboard"))
        sm.add_screen(Orion(name="orion"))
        sm.add_screen(TSCU(name="tscu"))

        # Bind to detect screen changes and reset the clock update
        sm.bind(current=sm.on_current_screen)

        return sm


if __name__ == "__main__":
    MainApp().run()
