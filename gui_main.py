import os

from pages.Inverter import Inverter

os.environ['KIVY_NO_FILELOG'] = '1'  # eliminate file log

from kivy.clock import Clock
from pages.Dash import Dash
from kivy.app import App
from kivy.core.window import Window
from screen_switcher.screen_switcher import CustomScreenSwitcher  # Renamed to CentralizedScreenSwitcher


Window.fullscreen = 'auto'  # Enable fullscreen


class CentralizedScreenSwitcher(CustomScreenSwitcher):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.clock_event = None

    def on_current_screen(self, *args):
        # Cancel any existing clock event before starting a new one
        if self.clock_event:
            self.clock_event.cancel()

        # Start a new clock event that updates the currently active screen
        self.clock_event = Clock.schedule_interval(self.update_active_screen, 0.5) # 0.016 60fps

    def update_active_screen(self, dt):
        # Call a `refresh` method on the active screen, if it exists
        if hasattr(self.current_screen, "refresh"):
            self.current_screen.refresh()


class MainApp(App):
    def build(self):
        # Use CentralizedScreenSwitcher instead of the default CustomScreenSwitcher
        sm = CentralizedScreenSwitcher()

        # Add screens to the manager
        sm.add_screen(Inverter(name="inverter"))
        sm.add_screen(Dash(name="dashboard"))
        #sm.add_screen(DebugScreen(name="debug"))

        # Bind to detect screen changes and reset the clock update
        sm.bind(current=sm.on_current_screen)

        return sm

if __name__ == "__main__":
    MainApp().run()
