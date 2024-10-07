# main.py
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from Pages.Speed_page import SpeedPage  # Import the SpeedPage and Speeddata class

class MainScreen(Screen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        # Create an instance of SpeedPage and add it to the screen
        self.speed_page = SpeedPage()
        self.add_widget(self.speed_page)


class SpeedApp(App):
    def build(self):
        # Create a ScreenManager and add the MainScreen
        sm = ScreenManager()
        sm.add_widget(MainScreen(name='main'))
        return sm

if __name__ == '__main__':
    SpeedApp().run()
