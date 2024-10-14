from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.progressbar import ProgressBar
from kivy.uix.label import Label
from kivy.graphics import Color, RoundedRectangle, Rectangle
from kivy.clock import Clock


class CustomProgressBar(ProgressBar):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.height = 10
        self.bind(value=self.update_canvas)

    def update_canvas(self, *args):
        self.canvas.clear()
        with self.canvas:
            # Draw the background of the progress bar
            Color(0.3, 0.3, 0.3, 1)  # Dark Gray Background
            RoundedRectangle(pos=self.pos, size=self.size, radius=[10])

            # Draw the custom filled part of the progress bar
            fill_ratio = self.width * (self.value / self.max)
            Color(0.2, 0.6, 0.8, 1)  # Blue Gradient Fill
            RoundedRectangle(pos=self.pos, size=(fill_ratio, self.height), radius=[10])


class CustomProgressBarApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)

        # Create a label to display the progress value
        self.label = Label(text="Progress: 0%", font_size='10sp')
        layout.add_widget(self.label)

        # Create the custom progress bar
        self.progress_bar = CustomProgressBar(max=100, value=0)
        layout.add_widget(self.progress_bar)

        # Schedule the value change
        Clock.schedule_interval(self.increment_value, 0.1)

        return layout

    def increment_value(self, dt):
        if self.progress_bar.value >= 100:
            self.progress_bar.value = 0
        self.progress_bar.value += 1
        self.label.text = f"Progress: {self.progress_bar.value}%"


if __name__ == '__main__':
    CustomProgressBarApp().run()
