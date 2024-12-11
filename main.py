# main.py

from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from pages.Dash import Dash

from pages.DriverDashboard import DriverDashboard
from pages.Inverter import Inverter
#from pages.Debug import DebugScreen
from screen_switcher.screen_switcher import CustomScreenSwitcher  # Renamed to CentralizedScreenSwitcher
# Config window size
Window.size = (1024, 600)

Window.minimum_width, Window.minimum_height = (1024, 600)

class CentralizedScreenSwitcher(CustomScreenSwitcher):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.clock_event = None

    def on_current_screen(self, *args):
        # Cancel any existing clock event before starting a new one
        if self.clock_event:
            self.clock_event.cancel()

        # Start a new clock event that updates the currently active screen
        self.clock_event = Clock.schedule_interval(self.update_active_screen, 0.01)

    def update_active_screen(self, dt):
        # Call a `refresh` method on the active screen, if it exists
        if hasattr(self.current_screen, "refresh"):
            self.current_screen.refresh()

class DriverDash(App):
    def build(self):
        # Use CentralizedScreenSwitcher instead of the default CustomScreenSwitcher
        sm = CentralizedScreenSwitcher()

        # Add screens to the manager
        sm.add_screen(Dash(name="dashboard"))
        sm.add_screen(Inverter(name="inverter"))
        #sm.add_screen(DebugScreen(name="debug"))

        # Bind to detect screen changes and reset the clock update
        sm.bind(current=sm.on_current_screen)

        return sm

if __name__ == "__main__":
    DriverDash().run()
