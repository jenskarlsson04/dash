from kivy.uix.widget import Widget
from kivy.graphics import Rectangle, Color
from kivy.properties import StringProperty, BooleanProperty, NumericProperty


class BatteryWidget(Widget):
    # battery_color = StringProperty("green")  # Dynamic property for the color (no longer needed)
    show_terminal = BooleanProperty(True)  # Toggle for showing the terminal
    show_outline = BooleanProperty(True)  # Toggle for showing the outline
    battery_level = NumericProperty(1.0)  # 0.0 to 1.0

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(pos=self.update_graphics, size=self.update_graphics)
        self.bind(
            # battery_color=self.update_graphics,  # No longer needed
            battery_level=self.update_graphics,
            show_terminal=self.update_graphics,
            show_outline=self.update_graphics,
        )
        self.update_graphics()

    def update_graphics(self, *args):
        """Draw the battery outline and fill dynamically based on size and battery_level."""
        self.canvas.clear()
        outline_width = self.width
        outline_height = self.height

        with self.canvas:
            if self.show_outline:
                # Draw battery outline
                Color(0.5, 0.5, 0.5, 1)  # Grey color
                Rectangle(pos=self.pos, size=(outline_width, outline_height))

            if self.show_terminal:
                # Draw battery terminal
                terminal_width = outline_width * 0.35
                terminal_height = outline_height * 0.15
                Rectangle(
                    pos=(
                        self.x + (outline_width - terminal_width) / 2,
                        self.top,
                    ),
                    size=(terminal_width, terminal_height),
                )

            # Determine color based on battery_level
            if self.battery_level >= 0.5:
                Color(0, 1, 0, 1)  # Green
            elif self.battery_level >= 0.2:
                Color(1, 0.65, 0, 1)  # Orange
            else:
                Color(1, 0, 0, 1)  # Red

            # Draw battery fill as vertical progress bar (bottom to top)
            fill_padding = 20
            fill_height = (outline_height - 2 * fill_padding) * self.battery_level
            Rectangle(
                pos=(self.x + fill_padding, self.y + fill_padding),
                size=(
                    outline_width - 2 * fill_padding,
                    fill_height,
                ),
            )

    # def update_color(self, color):
    #     """Update the battery fill color."""
    #     self.battery_color = color
