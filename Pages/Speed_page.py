from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.properties import NumericProperty

class SpeedPage(FloatLayout):
    # Define a NumericProperty to represent the speed value
    speed = NumericProperty(0)

    def __init__(self, **kwargs):
        super(SpeedPage, self).__init__(**kwargs)

        # Create a Label to display the speed
        self.speed_label = Label(
            text=f"Speed: {self.speed}",  # Show the speed value
            font_size='24sp',
            size_hint=(0.3, 0.3),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )

        # Bind the label text to update when the speed value changes
        self.bind(speed=lambda instance, value: setattr(self.speed_label, 'text', f"Speed: {value}"))

        # Add the label to the layout
        self.add_widget(self.speed_label)
