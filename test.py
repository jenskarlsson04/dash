from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
from random import choice
from datetime import datetime


class ErrorLogScreen(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'

        # Scrollable area for error messages
        scroll_view = ScrollView(size_hint=(1, 0.9))
        self.error_list = BoxLayout(orientation='vertical', size_hint_y=None)
        self.error_list.bind(minimum_height=self.error_list.setter('height'))
        scroll_view.add_widget(self.error_list)

        # Example error messages to randomly display
        self.errors = [
            "BMS: over-temperature",
            "BMS: over-voltage",
            "MOTOR TEMP: 90% of critical level",
            "SHUTDOWN CIRCUIT: open"
        ]

        # Add title header
        header = BoxLayout(size_hint_y=None, height=40)
        header.add_widget(Label(text="[b]Error message[/b]", markup=True, color=(0, 1, 1, 1), size_hint_x=0.8))
        header.add_widget(Label(text="[b]Time[/b]", markup=True, color=(0, 1, 1, 1), size_hint_x=0.2))
        self.add_widget(header)

        # Add scroll view to the layout
        self.add_widget(scroll_view)

        # Schedule a function to update the error log every few seconds
        Clock.schedule_interval(self.update_log, 2)

    def update_log(self, dt):
        # Pick a random error message
        error_message = choice(self.errors)

        # Get the current time
        current_time = datetime.now().strftime("%H:%M:%S")

        # Add new message with timestamp to the log
        log_entry = BoxLayout(size_hint_y=None, height=30)
        log_entry.add_widget(Label(text=error_message, size_hint_x=0.8))
        log_entry.add_widget(Label(text=current_time, size_hint_x=0.2))

        # Add the new log entry to the top of the list
        self.error_list.add_widget(log_entry, index=0)


class ErrorLogApp(App):
    def build(self):
        return ErrorLogScreen()


if __name__ == '__main__':
    ErrorLogApp().run()
