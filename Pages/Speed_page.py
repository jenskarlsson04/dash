# speed_page.py

from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.properties import StringProperty
from setuptools.command.build_ext import if_dl

from canReader import SpeedData, canReader


class SpeedPage(FloatLayout):
    # Create a StringProperty to hold the speed value for dynamic updates
    speed_value = StringProperty("0")

    def __init__(self, **kwargs):
        super(SpeedPage, self).__init__(**kwargs)

        # Create a label to display the speed value
        self.speed_label = Label(text=self.speed_value, size_hint=(.2, .1), pos_hint={'x': .4, 'y': .5}, font_size=48)
        self.add_widget(self.speed_label)

        # Bind the label's text to the speed_value property for dynamic updates
        self.bind(speed_value=self.update_speed_label)

        # Schedule UI updates every 0.5 seconds
        Clock.schedule_interval(self.update_ui, 0.5)

    def update_speed_label(self, instance, value):
        """
        Update the label whenever speed_value changes.
        """
        print(f"Updating speed label to: {value}")  # Debug statement
        self.speed_label.text = value

    def update_ui(self, dt):
        """
        This method will be called periodically to update the UI based on new CAN data.
        """
        # Read new data from the CAN reader
        Data = canReader.read_message()
        print(f"Received data: {Data}")  # Debug statement to show received data

        # Use pattern matching to handle the data based on its type and attributes
        if isinstance(Data, SpeedData):
            # Update the speed_value property with the extracted speed value
            self.speed_value = str(Data.speed)
        else:
            print(f"Received unknown data type: {type(Data)}")
            self.speed_value = "0"