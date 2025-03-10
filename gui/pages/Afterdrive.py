import random

# Import kivy
from kivy.uix.scrollview import ScrollView
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup
from kivy.core.window import Window

# Import lap time handler
from gui.pages.time_table_manager import TimeTableManager

# Import Custom widgets
from gui.widgets import CustomProgressBar
from gui.widgets import OutlinedBox
from gui.widgets import BatteryWidget

# Import can stuff
import canparser
from can_reader import subscribe_can_message

# Import error messages and CAN data
from gui.shared_data import SharedDataDriver
from stats.Stats import Stats


# Main Dashboard Page
class Afterdrive(Screen):
    def __init__(self, **kwargs):
        super(Afterdrive, self).__init__(**kwargs)
        self.Stats = Stats()

        root_layout = BoxLayout(orientation="vertical")

        # Use a main layout to contain the dashboard elements
        header = BoxLayout(orientation="vertical", size_hint=(1, 0.2))
        speed_bar = BoxLayout(orientation="horizontal")

        # Variabler för data hämtat från JSON

        # current_stats = stats.get_stats()

        # Tilldela värden till separata variabler
        # orion_current_max = current_stats["orion_current_max"]
        # speed_max = current_stats["speed_max"]
        # pack_temp_max = current_stats["pack_temp_max"]
        # lv_bat_voltage_min = current_stats["lv_bat_voltage_min"]
        # pack_voltage_min = current_stats["pack_voltage_min"]
        # power_max = current_stats["power_max"]
        # total_run_time = current_stats["total_run_time"]
        # driving_time = current_stats["driving_time"]
        # consumed_soc = current_stats["consumed_soc"]
        # energy_drawn_kwh = current_stats["energy_drawn_kwh"]
        # distance_driven_m = current_stats["distance_driven_m"]

        # Add custom progress bars at the top of the screen
        self.top_progress_bar1 = CustomProgressBar(
            size_hint=(0.33, 1),
            pos_hint={"x": 0, "y": 0},
            threshold=0,
            max_value=40,
            default_color=(0, 1, 0, 1),
        )
        self.top_progress_bar2 = CustomProgressBar(
            size_hint=(0.33, 1),
            pos_hint={"x": 0.33, "y": 0},
            threshold=40,
            max_value=80,
            default_color=(1, 0.65, 0, 1),
        )
        self.top_progress_bar3 = CustomProgressBar(
            size_hint=(0.33, 1),
            pos_hint={"x": 0.60, "y": 0},
            threshold=80,
            max_value=120,
            default_color=(1, 0, 0, 1),
        )
        speed_bar.add_widget(self.top_progress_bar1)
        speed_bar.add_widget(self.top_progress_bar2)
        speed_bar.add_widget(self.top_progress_bar3)
        header.add_widget(speed_bar)
        root_layout.add_widget(header)

        main_layout = BoxLayout(orientation="horizontal", spacing=10)
        root_layout.add_widget(main_layout)

        # Left section
        left_section = OutlinedBox(
            orientation="vertical", spacing=10, size_hint=(0.33, 1)
        )

        left_upper = OutlinedBox(
            orientation="vertical", spacing=10, size_hint=(1, 0.33)
        )


        left_middle = OutlinedBox(
            orientation="vertical", spacing=10, size_hint=(1, 0.33)
        )


        left_lower = OutlinedBox(
            orientation="vertical", spacing=10, size_hint=(1, 0.33)
        )


        left_section.add_widget(left_upper)
        left_section.add_widget(left_middle)
        left_section.add_widget(left_lower)
        main_layout.add_widget(left_section)

        # Middle section
        middle_section = OutlinedBox(
            orientation="vertical", spacing=10, size_hint=(0.33, 1)
        )
        middle_upper = OutlinedBox(
            orientation="vertical", spacing=10, size_hint=(1, 0.7)
        )

        middle_lower = OutlinedBox(
            orientation="vertical", spacing=10, size_hint=(1, 0.345)
        )

        middle_section.add_widget(middle_upper)
        middle_section.add_widget(middle_lower)
        main_layout.add_widget(middle_section)

        # Right section
        right_section = OutlinedBox(
            orientation="vertical", spacing=10, size_hint=(0.33, 1)
        )
        right_upper = OutlinedBox(
            orientation="vertical", spacing=10, size_hint=(1, 0.7)
        )

        right_lower = OutlinedBox(
            orientation="vertical", spacing=10, size_hint=(1, 0.345)
        )

        right_section.add_widget(right_upper)
        right_section.add_widget(right_lower)
        main_layout.add_widget(right_section)

        self.add_widget(root_layout)

    def refresh(self):
        pass



    def _update_text_size(self, instance, value):
        # Set text_size to the width only so the text does not wrap vertically
        instance.text_size = (instance.width, None)


# Main App Class
class AfterdriveApp(App):
    def build(self):
        return Afterdrive()


if __name__ == "__main__":
    AfterdriveApp().run()
