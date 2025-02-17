from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, Rectangle
from kivy.uix.label import Label
from kivy.properties import BooleanProperty


class Statusbar(FloatLayout):
    """Widget for the status bar with dynamic color and text based on a boolean status."""

    status = BooleanProperty(False)  # Default status is False (Disconnected)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(status=self.update_bar)  # Update the bar when the status changes
        self.draw_bar()

    def draw_bar(self):
        """Draw the initial bar."""
        with self.canvas:
            # Set initial color (red for Disconnected)
            self.color = Color(1, 0, 0, 1)  # Default color is red
            self.bar = Rectangle(pos=self.pos, size=(self.width, self.height))

        self.bind(pos=self.update_bar_position, size=self.update_bar_position)

        # Add a label for the status text
        self.status_label = Label(
            text="Systems: Disconnected",  # Default text
            size_hint=(None, None),
            font_size=50,
            halign="center",
            valign="middle",
            color=(1, 1, 1, 1),  # White text
        )
        self.add_widget(self.status_label)
        self.update_label_position()

    def update_bar_position(self, *args):
        """Update the bar's position and size."""
        self.bar.pos = self.pos
        self.bar.size = self.size
        self.update_label_position()

    def update_label_position(self):
        """Center the label inside the bar."""
        self.status_label.pos_hint = {"center_x": 0.5, "center_y": 0.5}

    def update_bar(self, *args):
        """Change the bar's color and update the label text based on the boolean status."""
        if self.status:  # True = Connected
            self.color.rgb = (0, 1, 0)  # Green
            self.status_label.text = "Systems: Connected!"
        else:  # False = Disconnected
            self.color.rgb = (1, 0, 0)  # Red
            self.status_label.text = "Systems: Disconnected!"
