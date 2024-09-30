# speed_page.py
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.properties import StringProperty


# Simulated Speeddata class structure for demonstration
class Speeddata:
    def __init__(self, speed):
        self.speed = speed


class SpeedPage(FloatLayout):
    # Create a StringProperty to hold the speed value for dynamic updates
    speed_value = StringProperty("0")

    def __init__(self, **kwargs):
        super(SpeedPage, self).__init__(**kwargs)

        # Create a label to display the speed value
        self.speed_label = Label(text=self.speed_value, size_hint=(.2, .1), pos_hint={'x': .4, 'y': .5}, font_size=48)
        self.add_widget(self.speed_label)

        # Bind the label's text to the speed_value property
        self.bind(speed_value=self.update_speed_label)

    def update_speed_label(self, instance, value):
        """
        Update the label whenever speed_value changes.
        """
        self.speed_label.text = value

    def process_can_data(self, data):
        """
        This method will be called whenever new CAN data is received.
        It expects a Speeddata object and will use match-case to handle it.
        """
        # Use a match-case to handle the data based on its type and attributes
        match data:
            case Speeddata(speed=speed):
                # Update the speed_value property with the extracted speed value
                self.speed_value = str(speed)
            case _:
                # Default action if the data is not a recognized Speeddata instance
                print(f"Received unknown data type: {type(data)}")
