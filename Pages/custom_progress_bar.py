from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle


class CustomProgressBar(Widget):
    def __init__(self, value=100, max_value=100, intervals=True, green_threshold=40, orange_threshold=20, **kwargs):
        """
        Customizable Progress Bar with dynamic color changes based on thresholds.

        :param value: Current value of the progress bar (0-100).
        :param max_value: Maximum value of the progress bar (default 100).
        :param intervals: Whether to use color intervals (True/False).
        :param green_threshold: Percentage at which the bar is green (default 40%).
        :param orange_threshold: Percentage at which the bar turns orange (default 20%).
        :param kwargs: Other standard Kivy widget options (e.g., size, position).
        """
        super(CustomProgressBar, self).__init__(**kwargs)
        self.value = value
        self.max_value = max_value
        self.intervals = intervals
        self.green_threshold = green_threshold
        self.orange_threshold = orange_threshold ## When under orange it turns red.
        self.canvas_color = (0, 1, 0, 1)  # Default color is green

        self.bind(pos=self.update_progress, size=self.update_progress)

    def set_value(self, value):
        """Update the progress bar value."""
        self.value = value
        self.update_progress()

    def update_progress(self, *args):
        """Redraw the progress bar and update its color based on thresholds."""
        if self.intervals:
            # Determine the color based on the current percentage value
            if self.value > self.green_threshold:
                self.canvas_color = (0, 1, 0, 1)  # Green when above green_threshold
            elif self.orange_threshold < self.value <= self.green_threshold:
                self.canvas_color = (1, 0.65, 0, 1)  # Orange between orange_threshold and green_threshold
            else:
                self.canvas_color = (1, 0, 0, 1)  # Red when below orange_threshold
        else:
            # Single color (green) when intervals are not used
            self.canvas_color = (0, 1, 0, 1)  # Green if intervals are disabled

        # Draw the custom progress bar
        with self.canvas:
            self.canvas.clear()
            Color(*self.canvas_color)
            Rectangle(pos=self.pos, size=(self.width * (self.value / self.max_value), self.height))

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
