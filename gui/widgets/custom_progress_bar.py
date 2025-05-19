from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle


class CustomProgressBar(Widget):
    def __init__(
        self,
        value=100,
        max_value=100,
        min_value=0,
        threshold=0,
        intervals=False,
        green_threshold=40,
        orange_threshold=20,
        default_color=(0, 1, 0, 1),
        **kwargs
    ):
        """
        Customizable Progress Bar with dynamic color changes based on thresholds and a custom default color.

        :param value: Current value of the progress bar (0-100).
        :param max_value: Maximum value of the progress bar (default 100).
        :param min_value: Minimum value of the progress bar (default 0).
        :param threshold: The value below which the bar should not render.
        :param intervals: Whether to use color intervals (True/False).
        :param green_threshold: Percentage at which the bar is green (default 40%).
        :param orange_threshold: Percentage at which the bar turns orange (default 20%).
        :param default_color: Custom default color for the progress bar in RGBA (default is green).
        :param kwargs: Other standard Kivy widget options (e.g., size, position).
        """
        super(CustomProgressBar, self).__init__(**kwargs)
        self.value = value
        self.max_value = max_value
        self.min_value = min_value
        self.threshold = threshold  # The value below which the bar is not rendered
        self.intervals = intervals
        self.green_threshold = green_threshold
        self.orange_threshold = orange_threshold  # When under orange it turns red
        self.default_color = default_color  # Custom color if intervals are disabled
        self.canvas_color = default_color  # Initialize with the default color

        # Initialize the canvas instructions for the progress bar
        with self.canvas:
            self._color_instruction = Color(*self.default_color)
            self._rect = Rectangle(pos=self.pos, size=(0, self.height))

        self.bind(pos=self.update_progress, size=self.update_progress)

    def set_value(self, value):
        """
        Update the progress bar value, ensuring it remains between min_value and max_value,
        and handle the behavior when the value is below the threshold.
        """
        self.value = max(
            min(value, self.max_value), self.min_value
        )  # Clamp value within [min_value, max_value]
        self.update_progress()

    def update_progress(self, *args):
        """Redraw the progress bar and update its color based on thresholds."""
        if self.value < self.threshold:
            self._rect.size = (0, self.height)
            return

        adjusted_value = self.value - self.threshold
        adjusted_max = self.max_value - self.threshold
        progress_percentage = adjusted_value / adjusted_max

        if self.intervals:
            if self.value > self.green_threshold:
                color = (0, 1, 0, 1)
            elif self.orange_threshold < self.value <= self.green_threshold:
                color = (1, 0.65, 0, 1)
            else:
                color = (1, 0, 0, 1)
        else:
            color = self.default_color

        self._color_instruction.rgba = color
        self._rect.pos = self.pos
        self._rect.size = (self.width * progress_percentage, self.height)

    def configure_intervals(self, green_threshold, orange_threshold, intervals=True):
        """
        Configure the color intervals for the progress bar.

        :param green_threshold: Percentage at which the bar is green.
        :param orange_threshold: Percentage at which the bar turns orange.
        :param intervals: Whether to use intervals or not.
        """
        self.green_threshold = green_threshold
        self.orange_threshold = orange_threshold
        self.intervals = intervals
        self.update_progress()

    def set_default_color(self, color):
        """
        Set a custom default color for the progress bar.

        :param color: A tuple representing the color in RGBA (e.g., (1, 0, 0, 1) for red).
        """
        self.default_color = color
        self.update_progress()
