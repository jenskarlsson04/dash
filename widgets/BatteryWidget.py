from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Rectangle, Color


class BatteryWidget(FloatLayout):
    """Widget for the battery symbol with dynamic color."""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.battery_color = "green"  # Initial color
        self.draw_battery()

    def draw_battery(self):
        """Draw the battery outline and fill dynamically based on size."""
        self.canvas.clear()
        outline_width = self.width
        outline_height = self.height

        with self.canvas:
            # Draw battery outline
            Color(0.5, 0.5, 0.5, 1)  # Grey color
            self.outline = Rectangle(
                pos=(self.x, self.y), size=(outline_width, outline_height)
            )

            # Draw battery terminal
            terminal_width = outline_width * 0.1
            terminal_height = outline_height * 0.3
            self.terminal = Rectangle(
                pos=(self.x + outline_width, self.y + (outline_height - terminal_height) / 2),
                size=(terminal_width, terminal_height),
            )

            # Set the battery fill color
            if self.battery_color == "green":
                Color(0, 1, 0, 1)  # Green
            elif self.battery_color == "orange":
                Color(1, 0.65, 0, 1)  # Orange
            elif self.battery_color == "red":
                Color(1, 0, 0, 1)  # Red

            # Draw battery fill (always full)
            fill_padding = 5  # Add padding inside the outline
            self.fill = Rectangle(
                pos=(self.x + fill_padding, self.y + fill_padding),
                size=(outline_width - 2 * fill_padding, outline_height - 2 * fill_padding),
            )

    def update_color(self, color):
        """Update the battery fill color."""
        self.battery_color = color
        self.draw_battery()