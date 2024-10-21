# main.py
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.config import Config
from kivy.core.window import Window

# Set window size
Config.set("graphics", "width", "1024")
Config.set("graphics", "height", "600")
Config.set("graphics", "resizable", "0")   # Disable resizing
Config.write()

# Alternatively, you can set it using the Window object
Window.size = (1024, 600)


# Define the first screen
class ScreenOne(Screen):
    def __init__(self, **kwargs):
        super(ScreenOne, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')

        # Add a button to switch to ScreenTwo
        switch_btn = Button(text='Go to Screen Two', size_hint=(0.3, 0.2))
        switch_btn.bind(on_press=self.switch_to_screen_two)

        layout.add_widget(switch_btn)
        self.add_widget(layout)

    def switch_to_screen_two(self, instance):
        self.manager.current = 'screen_two'


# Define the second screen
class ScreenTwo(Screen):
    def __init__(self, **kwargs):
        super(ScreenTwo, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')

        # Add a button to switch back to ScreenOne
        switch_btn = Button(text='Go to Screen One', size_hint=(0.3, 0.2))
        switch_btn.bind(on_press=self.switch_to_screen_one)

        layout.add_widget(switch_btn)
        self.add_widget(layout)

    def switch_to_screen_one(self, instance):
        self.manager.current = 'screen_one'


# Create the main application class
class MyScreenApp(App):
    def build(self):
        sm = ScreenManager()

        # Add screens to the ScreenManager
        sm.add_widget(ScreenOne(name='screen_one'))
        sm.add_widget(ScreenTwo(name='screen_two'))

        return sm


if __name__ == '__main__':
    MyScreenApp().run()
