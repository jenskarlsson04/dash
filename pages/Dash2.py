import random
from kivy.uix.scrollview import ScrollView
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import Screen
from pages.time_table_manager import TimeTableManager
from widgets.custom_progress_bar import CustomProgressBar
from widgets.OutlinedBox import OutlinedBox
from widgets.BatteryWidget import BatteryWidget
from widgets.Statusbar import Statusbar
import canparser
from can_reader import subscribe_can_message
from kivy.graphics import Color, Line


# Main Dashboard Page
class Dash2(Screen):
    def __init__(self, **kwargs):
        super(Dash2, self).__init__(**kwargs)
        # Initialize Time Table Manager

        # Can subscribtions

        subscribe_can_message(canparser.AnalogCanConverterSensorReadingsDataF, self.update_speed)
        subscribe_can_message(canparser.VcuStateData, self.update_status)
       # subscribe_can_message(canparser.OrionPowerData, self.update_soc)





        self.time_table_manager = TimeTableManager(total_laps=22)

        # Variables to update
        self.speed = 80
        self.soc = 0  # Track remaining SOC
        self.last_soc = 0  # Track SOC at the start of the lap
        self.lap_counter = 0  # Track total number of laps
        self.laps = 22
        self.lvbat = 12
        self.state = "N/A"
        self.errors = ["Hej igen", "fixa", "error hanterare"]

        root_layout = BoxLayout(orientation='vertical')

        # Use a main FloatLayout to contain the dashboard elements


        header = BoxLayout(orientation='vertical', size_hint=(1, 0.2))

        speed_bar = BoxLayout(orientation='horizontal')


        # Add a custom progress bar at the top of the screen
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
        # Add the speedbar to the mainlayout


        header.add_widget(speed_bar)

        root_layout.add_widget(header)


        main_layout = BoxLayout(orientation='horizontal', spacing=10)
        root_layout.add_widget(main_layout)


        left_section = OutlinedBox(orientation='vertical', spacing=10, size_hint=(0.33, 1))

        # Upper left section, used for speed for example

        left_upper = OutlinedBox(orientation='vertical', spacing=10, size_hint=(1, 0.33))

        self.lastlap_text_label = Label(
            text="LAST LAP",
            font_size="50sp",
            halign="center",
            valign="top",
            size_hint=(1, 0.4),
            color=(0, 1, 1, 1),
        )
        self.lastlap_text_label.bind(size=self._update_text_size)
        left_upper.add_widget(self.lastlap_text_label)

        # Speed value

        lastlap_value_layout = BoxLayout(
            orientation="horizontal", size_hint=(1, 0.4), spacing=5
        )
        self.lastlap_value_label = Label(
            text="--:--:--",
            font_size="60sp",
            halign="left",
            valign="middle",
            size_hint_x=0.3,
            width=170,  # Fast bredd så att värdet ser konsekvent ut
            color=(1, 1, 1, 1),
        )
        lastlap_value_layout.bind(size=self._update_text_size)
        lastlap_value_layout.add_widget(self.lastlap_value_label)
        left_upper.add_widget(lastlap_value_layout)



        # Left middle used for LV bat

        left_middle = OutlinedBox(orientation='vertical', spacing=10, size_hint=(1, 0.33))

        # Speed

        self.speed_text_label = Label(
            text="SPEED",
            font_size="50sp",
            halign="center",
            valign="top",
            size_hint=(1, 0.4),
            color=(0, 1, 1, 1),
        )
        self.speed_text_label.bind(size=self._update_text_size)
        left_middle.add_widget(self.speed_text_label)

        # Speed value

        speed_value_layout = BoxLayout(
            orientation="horizontal", size_hint=(1, 0.4), spacing=5
        )
        self.speed_value_label = Label(
            text="N/A",
            font_size="80sp",
            halign="left",
            valign="middle",
            size_hint_x=0.3,
            width=170,  # Fast bredd så att värdet ser konsekvent ut
            color=(1, 1, 1, 1),
        )
        speed_value_layout.bind(size=self._update_text_size)
        speed_value_layout.add_widget(self.speed_value_label)
        left_middle.add_widget(speed_value_layout)


        # Add maybe a APPS and breakpressure bar? ( I think that is useless )

        left_lower = OutlinedBox(orientation='vertical', spacing=10, size_hint=(1, 0.33))





        # Add the upper, middle and lower sections to left layout

        left_section.add_widget(left_upper)
        left_section.add_widget(left_middle)
        left_section.add_widget(left_lower)

        # Add the left section to the mainlayout

        main_layout.add_widget(left_section)




        middle_section = OutlinedBox(orientation='vertical', spacing=10, size_hint=(0.33, 1))

        middle_upper = OutlinedBox(orientation='vertical', spacing=10, size_hint=(1, 0.7))

        # VCU Status

        middle_lower = OutlinedBox(orientation='vertical', spacing=10, size_hint=(1, 0.345))

        self.status_text_label = Label(
            text="STATUS",
            font_size="50sp",
            halign="center",
            valign="top",
            size_hint=(1, 0.4),
            color=(0, 1, 1, 1),
        )
        self.status_text_label.bind(size=self._update_text_size)
        middle_lower.add_widget(self.status_text_label)

        # Speed value

        status_value_layout = BoxLayout(
            orientation="horizontal", size_hint=(1, 0.4), spacing=5
        )
        self.status_value_label = Label(
            text="N/A",
            font_size="80sp",
            halign="left",
            valign="middle",
            size_hint_x=0.3,
            width=170,  # Fast bredd så att värdet ser konsekvent ut
            color=(1, 1, 1, 1),
        )
        status_value_layout.bind(size=self._update_text_size)
        status_value_layout.add_widget(self.status_value_label)
        middle_lower.add_widget(status_value_layout)

        # Add the upper and lower section to the middle section

        middle_section.add_widget(middle_upper)
        middle_section.add_widget(middle_lower)

        # Add the middle section to the main layout

        main_layout.add_widget(middle_section)

        right_section = OutlinedBox(orientation='vertical', spacing=10, size_hint=(0.33, 1))


        ## Faults, this page should have a own logic comparing the most important values and giving out
        # errors if something's wrong.


        right_upper = OutlinedBox(orientation='vertical', spacing=10, size_hint=(1, 0.7))


        error_title_layout = BoxLayout(
            orientation="horizontal", size_hint=(1, 0.2), spacing=10
        )
        self.errors_label = Label(
            text="Errors",
            font_size="45sp",
            halign="center",
            valign="middle",
            size_hint_x=0.7,
            color=(0, 1, 1, 1),
        )
        error_title_layout.add_widget(self.errors_label)
        self.errors_amount_label = Label(
            text="(0)",
            font_size="45sp",
            halign="left",
            valign="middle",
            size_hint_x=0.5,
            color=(0, 1, 1, 1),
        )
        error_title_layout.add_widget(self.errors_amount_label)
        right_upper.add_widget(error_title_layout)


        self.scroll_view_errors = ScrollView(
            size_hint=(1, 0.8), do_scroll_x=False, do_scroll_y=False
        )
        self.errors_content_layout = BoxLayout(
            orientation="vertical", spacing=10, size_hint_y=None,
        )
        self.errors_content_layout.bind(
            minimum_height=self.errors_content_layout.setter("height")
        )
        self.scroll_view_errors.add_widget(self.errors_content_layout)
        right_upper.add_widget(self.scroll_view_errors)


        right_lower = OutlinedBox(orientation='vertical', spacing=10, size_hint=(1, 0.345))

        self.LV_text_label = Label(
            text="LV BAT",
            font_size="50sp",
            halign="center",
            valign="top",
            size_hint=(1, 0.4),
            color=(0, 1, 1, 1),
        )
        self.LV_text_label.bind(size=self._update_text_size)
        right_lower.add_widget(self.LV_text_label)

        # Speed value

        LVBAT_value_layout = BoxLayout(
            orientation="horizontal", size_hint=(1, 0.4), spacing=5
        )
        self.LV_value_label = Label(
            text="N/A",
            font_size="80sp",
            halign="left",
            valign="middle",
            size_hint_x=0.3,
            width=170,  # Fast bredd så att värdet ser konsekvent ut
            color=(1, 1, 1, 1),
        )
        LVBAT_value_layout.bind(size=self._update_text_size)
        LVBAT_value_layout.add_widget(self.LV_value_label)
        right_lower.add_widget(LVBAT_value_layout)

        # Add the upper, middle and lower sections to the right section

        right_section.add_widget(right_upper)
        right_section.add_widget(right_lower)

        # Add the right section to the main layout
        main_layout.add_widget(right_section)



        self.add_widget(root_layout)



    def refresh(self):
        self.top_progress_bar1.set_value(self.speed)
        self.top_progress_bar2.set_value(self.speed)
        self.top_progress_bar3.set_value(self.speed)

        # Old laptime logic #
        new_lap_time = self.generate_random_time()
        self.time_table_manager.add_lap_time(new_lap_time)
        last_lap_color = self.time_table_manager.compare_last_lap(new_lap_time)
        self.lastlap_value_label.color = (
            (0, 1, 0, 1) if last_lap_color == "green" else (1, 0.85, 0, 1)
        )
        ##########################

        # Uppdatera fel

        # Uppdatera fel
        error_count = len(self.errors)
        self.errors_amount_label.text = f"({error_count})"
        self.errors_content_layout.clear_widgets()
        errors_to_show = self.errors[:4]
        for i, error in enumerate(errors_to_show):
            label = Label(
                text=error,
                font_size="35sp",
                size_hint_y=None,
                height=60,  # increased height for better spacing
                halign="left",
                valign="middle",
                color=(1, 0, 0, 1),
            )
            label.bind(size=self._update_text_size)
            self.errors_content_layout.add_widget(label)
            if i < len(errors_to_show) - 1:
                spacer = Widget(size_hint_y=None, height=30)
                self.errors_content_layout.add_widget(spacer)


        self.lastlap_value_label.text = f"{self.format_time(new_lap_time)}"
        self.speed_value_label.text = f'{self.speed}'
        self.LV_value_label.text = f'{self.lvbat} V'
        self.status_value_label.text = f'{self.state}'


    def generate_random_time(self):
        """Generate a random time in milliseconds between 10 and 180 seconds."""
        return random.randint(10000, 180000)

    def format_time(self, time_in_ms):
        """Format time into mm:ss:ms (minutes:seconds:milliseconds)."""
        minutes = time_in_ms // 60000
        seconds = (time_in_ms % 60000) // 1000
        milliseconds = time_in_ms % 1000
        return f"{minutes:02}:{seconds:02}:{milliseconds:03}"

    def update_speed(self, message):
        rad_s = round(message.parsed_data.wheel_speed_l_rad_per_sec)
        self.speed = round(rad_s * 3.6 * 0.2032) # Rad/s to kmh converter with 8 inch wheels.
        self.lvbat = round(message.parsed_data.voltage_volts,1)

    def update_status(self, message):
        self.state = message.parsed_data.State

    #def update_soc(self, message):
     #   self.soc = round(100*message.parsed_data.pack_soc_ratio)
    def _update_text_size(self, instance, value):
        # Set text_size to the width only so the text does not wrap vertically
        instance.text_size = (instance.width, None)

# Main App Class
class DashboardApp(App):
    def build(self):
        return Dash2()


if __name__ == "__main__":
    DashboardApp().run()
