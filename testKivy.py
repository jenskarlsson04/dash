import time

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from datetime import datetime


class ClockApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical')

        # Label to show the time
        self.time_label = Label(font_size=50)
        self.layout.add_widget(self.time_label)

        # Schedule the clock update every second
        Clock.schedule_interval(self.update_time, 0.001)

        return self.layout

    def update_time(self, *args):
        # Get current time and update the label

        current_time = time.strftime('%H:%M:%S') + '.' + str(int(time.time() * 1000) % 1000).zfill(3)
        self.time_label.text = current_time


if __name__ == "__main__":
    ClockApp().run()
