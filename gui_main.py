import os
os.environ['KIVY_NO_FILELOG'] = '1'  # eliminate file log
from kivy.app import App
from pages.Dash2 import Dash2
from screen_switcher.screen_switcher import CustomScreenSwitcher  # Renamed to CentralizedScreenSwitcher


class MainApp(App):
    def build(self):
        # Use CentralizedScreenSwitcher instead of the default CustomScreenSwitcher
        sm = CustomScreenSwitcher()

        # Add screens to the screen manager
        sm.add_screen(Dash2(name="dashboard2"))
        #  sm.add_screen(DriverDashboard(name="dashboard"))
        #sm.add_screen(DebugScreen(name="debug"))

        # Bind to detect screen changes and reset the clock update
        sm.bind(current=sm.on_current_screen)

        return sm


if __name__ == "__main__":
    MainApp().run()
