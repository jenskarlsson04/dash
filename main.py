# main.py
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from Pages.Speed_page import SpeedPage, Speeddata  # Import the SpeedPage and Speeddata class

class MainScreen(Screen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        # Create an instance of SpeedPage and add it to the screen
        self.speed_page = SpeedPage()
        self.add_widget(self.speed_page)

        # Simulate CAN data reception by directly calling process_can_data
        # Replace this with real CAN data handler calls in your implementation
        self.speed_page.process_can_data(Speeddata(85))  # Example of Speeddata input

class SpeedApp(App):
    def build(self):
        # Create a ScreenManager and add the MainScreen
        sm = ScreenManager()
        sm.add_widget(MainScreen(name='main'))
        return sm

if __name__ == '__main__':
    SpeedApp().run()
