from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from random import choice
from datetime import datetime
from kivy.uix.screenmanager import Screen
from kivy.core.window import Window

# Set window size to 1024x600 for development on desktop (remove if deploying to a fixed screen device)
Window.size = (1024, 600)


class DebugScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Main layout for DebugScreen
        layout = FloatLayout()
        self.add_widget(layout)

        # Title label at the top
        title = Label(
            text="[b]Debug[/b]",
            markup=True,
            font_size=40,  # Larger font for prominent title
            color=(0.3, 0.6, 1, 1),
            size_hint=(None, None),
            pos_hint={'x': 0.05, 'top': 0.98}
        )
        layout.add_widget(title)

        # Header for the error log table
        header_layout = BoxLayout(orientation='horizontal', size_hint=(0.9, None), height=50,
                                  pos_hint={'x': 0.05, 'top': 0.88})
        header_layout.add_widget(Label(
            text="[b]Error message[/b]",
            markup=True,
            color=(0.3, 0.6, 1, 1),
            font_size=28,  # Larger font for headers
            size_hint_x=0.7
        ))
        header_layout.add_widget(Label(
            text="[b]Time[/b]",
            markup=True,
            color=(0.3, 0.6, 1, 1),
            font_size=28,  # Larger font for headers
            size_hint_x=0.3
        ))
        layout.add_widget(header_layout)

        # Scrollable area for error messages
        scroll_view = ScrollView(size_hint=(0.9, 0.75), pos_hint={'x': 0.05, 'top': 0.85})
        self.error_list = BoxLayout(orientation='vertical', size_hint_y=None, spacing=15)
        self.error_list.bind(minimum_height=self.error_list.setter('height'))
        scroll_view.add_widget(self.error_list)

        # Add the scroll view to the main layout
        layout.add_widget(scroll_view)

        # Example error messages
        self.errors = [
            "BMS: over-temperature",
            "BMS: over-voltage",
            "MOTOR TEMP: 90% of critical level",
            "SHUTDOWN CIRCUIT: open"
        ]

        # Schedule a function to update the error log every few seconds


    def refresh(self):
        # Pick a random error message
        error_message = choice(self.errors)

        # Get the current time with seconds
        current_time = datetime.now().strftime("%H:%M:%S")

        # Create a log entry layout with larger font sizes for better readability
        log_entry = BoxLayout(size_hint_y=None, height=50)  # Larger height for readability
        log_entry.add_widget(Label(
            text=error_message,
            font_size=30,  # Larger font for log entries
            color=(1, 1, 1, 1),
            size_hint_x=0.7
        ))
        log_entry.add_widget(Label(
            text=current_time,
            font_size=30,  # Larger font for log entries
            color=(1, 1, 1, 1),
            size_hint_x=0.3
        ))

        # Add the new log entry to the top of the list
        self.error_list.add_widget(log_entry, index=0)

        # Limit the number of entries displayed to avoid overfilling the screen
        if len(self.error_list.children) > 8:  # Adjusted for 1024x600 resolution with larger text
            self.error_list.remove_widget(self.error_list.children[-1])


# Standalone app to test DebugScreen
class DebugApp(App):
    def build(self):
        return DebugScreen(name="debug_screen")


if __name__ == '__main__':
    DebugApp().run()
