import random
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import Screen
from kivy.core.window import Window
from pages.time_table_manager import TimeTableManager
from widgets.custom_progress_bar import CustomProgressBar
from widgets.BatteryWidget import BatteryWidget
from widgets.Statusbar import Statusbar
from kivy.uix.image import Image
import os
import canparser
from can_reader import subscribe_can_message
from can_reader import publish_message


class Inverter(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Can subs
        subscribe_can_message(canparser.BrakePressureData, self.update_inverter_temp)


        # Variabler för data
        self.inverter_temp = 0

        # Use a main FloatLayout to contain the dashboard elements
        main_layout = FloatLayout()


# Main label

        self.inverter_label = Label(text='Inverter', font_size='50sp', size_hint=(0.2, 0.1),
                                  pos_hint={'x': 0, 'y': 0.85}, color=(0, 1, 1, 1))

        # Add the background logo (logo.png) with low opacity
        image_path = os.path.join('./images/logo.png')
        self.logo_image = Image(
            source=image_path,
            opacity=0.15,
            allow_stretch=True,
            keep_ratio=True,
            size_hint=(0.15, 0.15),  # Half the width and height of the screen
            pos_hint={'center_x': 0.5, 'center_y': 0.93}  # Center the image
        )
# Inverter Temp

        self.inverter_temp_label = Label(text='Inverter Temp', font_size='80sp', size_hint=(None, None),
                                    pos_hint={'x': 0.22, 'y': 0.69}, color=(0, 1, 1, 1))

        self.inverter_temp_value_label = Label(text='000 C', font_size='80sp', size_hint=(None, None),
                                        pos_hint={'x': 0.08, 'y': 0.54}, color=(1, 1, 1, 1))
# Motor temp

        self.motortemp_label = Label(text='Motor Temp', font_size='80sp', size_hint=(None, None),
                                    pos_hint={'x': 0.19, 'y': 0.39}, color=(0, 1, 1, 1))
        self.motortemp_value_label = Label(text='000 C', font_size='80sp', size_hint=(None, None),
                                             pos_hint={'x': 0.08, 'y': 0.23}, color=(1, 1, 1, 1))

# Errors
        self.errors_label = Label(text='Inverter Errors (0):', font_size='40sp', size_hint=(None, None),
                                    pos_hint={'x': 0.7, 'y': 0.9}, color=(0, 1, 1, 1))


# Main layout

        main_layout.add_widget(self.inverter_label)

        main_layout.add_widget(self.logo_image)

# Inveter Layout
        main_layout.add_widget(self.inverter_temp_label)
        main_layout.add_widget(self.inverter_temp_value_label)
# Motor layout
        main_layout.add_widget(self.motortemp_label)
        main_layout.add_widget(self.motortemp_value_label)

# Erros layout

        main_layout.add_widget(self.errors_label)


# Adds all the widgets to the main layout
        self.add_widget(main_layout)


    def refresh(self):
        self.inverter_temp_value_label.text = f'{self.inverter_temp}'


    def update_inverter_temp(self, message):
        self.inverter_temp = round(message.parsed_data.raw_adc)



# Main App Class
class InverterDebug(App):
    def build(self):
        Window.size = (1024, 600)  # Set a larger window size for better layout
        return Inverter()


if __name__ == '__main__':
    InverterDebug().run()