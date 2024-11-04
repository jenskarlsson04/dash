# ClockScreen.py

import random
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen


class ClockScreen(Screen):
    def __init__(self, **kwargs):
        Screen.__init__(self, **kwargs)

        # Label to display the random value
        self.random_label = Label(text="Random: 1", font_size="40sp", pos_hint={"center_x": 0.5, "center_y": 0.5})
        self.add_widget(self.random_label)
        self.clock_event = None


    def refresh(self, dt=None):
        # Generate a random value between 1 and 10 and update the label
        random_value = random.randint(1, 10)
        self.random_label.text = f"Random: {random_value}"
