from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from pages.DriverDashboard import DriverDashboard
from kivy.clock import Clock

from kivy.core.window import Window

# Set window size explicitly
Window.size = (1024, 600)


class DriverDash(App):
    def build(self):
        # Create a ScreenManager and add the MainScreen

        Clock.schedule_interval()

        sm = ScreenManager()
        sm.add_widget(DriverDashboard(name='main'))
        return sm


if __name__ == '__main__':
    DriverDash().run()
