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
from gui.widgets.time_table_manager import TimeTableManager

# Import Custom widgets
from gui.widgets import CustomProgressBar
from gui.widgets import OutlinedBox
from gui.widgets import BatteryWidget

# Import can stuff

# Import error messages and CAN data
from gui.shared_data import SharedDataDriver


class DismissablePopup(Popup):
    """
    A custom popup that dismisses when the "o" key is pressed.
    """

    def on_open(self):
        # Request the keyboard when the popup opens.
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        if self._keyboard:
            self._keyboard.bind(on_key_down=self._on_keyboard_down)

    def on_dismiss(self):
        # Unbind and release the keyboard when the popup is dismissed.
        if hasattr(self, "_keyboard") and self._keyboard:
            self._keyboard.unbind(on_key_down=self._on_keyboard_down)
            self._keyboard = None

    def _keyboard_closed(self):
        if hasattr(self, "_keyboard") and self._keyboard:
            self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        # Dismiss the popup when the "o" key is pressed.
        if keycode[1] == "o":
            self.dismiss()
        return True


# Main Dashboard Page
class Dash2(Screen):
    def __init__(self, **kwargs):
        super(Dash2, self).__init__(**kwargs)
        self.SharedData = SharedDataDriver()

        self.time_table_manager = TimeTableManager(total_laps=22)

        # Variables to update
        self.last_soc = 0  # Track SOC at the start of the lap
        self.lap_counter = 0  # Track total number of laps
        self.laps = 22
        self.lvbat = 12
        self.state = "N/A"

        # Disable error popup
        self.show_error = False

        # For controlling the error popup as a queue:
        self.error_popup = None
        self.pending_error_messages = []  # Queue for error messages (without a dot)
        self.shown_errors = (
            set()
        )  # Set of active errors (without a dot) that have already been popped

        root_layout = BoxLayout(orientation="vertical")

        # Use a main layout to contain the dashboard elements
        header = BoxLayout(orientation="vertical", size_hint=(1, 0.2))
        speed_bar = BoxLayout(orientation="horizontal")

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

        lastlap_value_layout = BoxLayout(
            orientation="horizontal", size_hint=(1, 0.4), spacing=5
        )
        self.lastlap_value_label = Label(
            text="--:--:--",
            font_size="60sp",
            halign="left",
            valign="middle",
            size_hint_x=0.3,
            width=170,
            color=(1, 1, 1, 1),
        )
        lastlap_value_layout.bind(size=self._update_text_size)
        lastlap_value_layout.add_widget(self.lastlap_value_label)
        left_upper.add_widget(lastlap_value_layout)

        left_middle = OutlinedBox(
            orientation="vertical", spacing=10, size_hint=(1, 0.33)
        )
        self.soc_text_label = Label(
            text="SOC",
            font_size="50sp",
            halign="center",
            valign="top",
            size_hint=(1, 0.4),
            color=(0, 1, 1, 1),
        )
        self.soc_text_label.bind(size=self._update_text_size)
        left_middle.add_widget(self.soc_text_label)

        soc_value_layout = BoxLayout(orientation="horizontal", size_hint=(1, 0.6))
        self.soc_value_label = Label(
            text="N/A",
            font_size="80sp",
            halign="left",
            valign="middle",
            size_hint_x=0.3,
            width=170,
            color=(1, 1, 1, 1),
        )
        soc_value_layout.bind(size=self._update_text_size)
        soc_value_layout.add_widget(self.soc_value_label)
        left_middle.add_widget(soc_value_layout)

        left_lower = OutlinedBox(
            orientation="vertical", spacing=10, size_hint=(1, 0.33)
        )
        self.speed_text_label = Label(
            text="SPEED",
            font_size="50sp",
            halign="center",
            valign="top",
            size_hint=(1, 0.28),
            color=(0, 1, 1, 1),
        )
        self.speed_text_label.bind(size=self._update_text_size)
        left_lower.add_widget(self.speed_text_label)

        speed_value_layout = BoxLayout(
            orientation="horizontal", size_hint=(1, 0.4), spacing=5
        )
        self.speed_value_label = Label(
            text="N/A",
            font_size="80sp",
            halign="left",
            valign="middle",
            size_hint_x=0.3,
            width=170,
            color=(1, 1, 1, 1),
        )
        speed_value_layout.bind(size=self._update_text_size)
        speed_value_layout.add_widget(self.speed_value_label)
        left_lower.add_widget(speed_value_layout)

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
        self.battery_widget = BatteryWidget(
            size_hint=(1, 1),
            show_terminal=False,
            show_outline=False,
        )
        middle_upper.add_widget(self.battery_widget)

        middle_lower = OutlinedBox(
            orientation="vertical", spacing=10, size_hint=(1, 0.345)
        )
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

        status_value_layout = BoxLayout(
            orientation="horizontal", size_hint=(1, 0.4), spacing=5
        )
        self.status_value_label = Label(
            text="N/A",
            font_size="43sp",
            halign="left",
            valign="middle",
            size_hint_x=0.3,
            width=170,
            color=(1, 1, 1, 1),
        )
        status_value_layout.bind(size=self._update_text_size)
        status_value_layout.add_widget(self.status_value_label)
        middle_lower.add_widget(status_value_layout)

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
            size_hint=(1, 0.9), do_scroll_x=False, do_scroll_y=False
        )
        self.errors_content_layout = BoxLayout(
            orientation="vertical", spacing=1, size_hint_y=None
        )
        self.errors_content_layout.bind(
            minimum_height=self.errors_content_layout.setter("height")
        )
        # Create a fixed pool of 4 reusable error labels and spacers
        self.error_labels = []
        for _ in range(4):
            label = Label(
                text="",
                font_size="35sp",
                size_hint_y=None,
                height=60,
                halign="center",
                valign="middle",
                color=(1, 1, 1, 1),
            )
            label.bind(size=self._update_text_size)
            self.error_labels.append(label)
            self.errors_content_layout.add_widget(label)
            spacer = Widget(size_hint_y=None, height=0)
            self.errors_content_layout.add_widget(spacer)
        self.scroll_view_errors.add_widget(self.errors_content_layout)
        right_upper.add_widget(self.scroll_view_errors)

        right_lower = OutlinedBox(
            orientation="vertical", spacing=10, size_hint=(1, 0.345)
        )
        self.LV_text_label = Label(
            text="LV BAT",
            font_size="50sp",
            halign="center",
            valign="top",
            size_hint=(1, 0.3),
            color=(0, 1, 1, 1),
        )
        self.LV_text_label.bind(size=self._update_text_size)
        right_lower.add_widget(self.LV_text_label)
        LVBAT_value_layout = BoxLayout(
            orientation="horizontal", size_hint=(1, 0.4), spacing=5
        )
        self.LV_value_label = Label(
            text="N/A",
            font_size="80sp",
            halign="left",
            valign="middle",
            size_hint_x=0.3,
            width=170,
            color=(1, 1, 1, 1),
        )
        LVBAT_value_layout.bind(size=self._update_text_size)
        LVBAT_value_layout.add_widget(self.LV_value_label)
        right_lower.add_widget(LVBAT_value_layout)

        right_section.add_widget(right_upper)
        right_section.add_widget(right_lower)
        main_layout.add_widget(right_section)

        self.add_widget(root_layout)

    def refresh(self):
        self.top_progress_bar1.set_value(self.SharedData.speed)
        self.top_progress_bar2.set_value(self.SharedData.speed)
        self.top_progress_bar3.set_value(self.SharedData.speed)

        # Old lap time logic
        new_lap_time = self.generate_random_time()
        result = self.time_table_manager.add_lap_time(new_lap_time)
        last_lap_color = self.time_table_manager.compare_last_lap(new_lap_time)
        self.lastlap_value_label.color = (
            (0, 1, 0, 1) if last_lap_color == "green" else (1, 0.85, 0, 1)
        )

        if not result["sufficient_soc"]:
            self.battery_widget.update_color("red")
        else:
            self.battery_widget.update_color("green")

        # Update errors
        error_count = len(self.SharedData.faults)
        self.errors_amount_label.text = f"({error_count})"
        errors_to_show = list(self.SharedData.faults)

        # Only consider errors without a dot for popups.
        active_errors = {err for err in errors_to_show if not err.startswith(".")}
        # Remove errors that have already been shown (permanently)
        active_errors = active_errors - self.shown_errors
        # For each active error not already pending, add it and mark it as shown.
        for err in active_errors:
            if err not in self.pending_error_messages:
                self.pending_error_messages.append(err)
                self.shown_errors.add(err)  # mark permanently as shown

        # If no popup is active, show the next pending error.
        if self.error_popup is None and self.pending_error_messages:
            self.show_next_error_popup()

        # Update the 4 reusable error labels
        for i in range(4):
            if i < len(errors_to_show):
                error = errors_to_show[i]
                label = self.error_labels[i]
                if error.startswith("."):
                    display_error = error[1:]
                    label.color = (1, 0.5, 0, 1)
                else:
                    display_error = error
                    label.color = (1, 0, 0, 1)
                label.text = display_error
            else:
                self.error_labels[i].text = ""

        # Update other values
        self.lastlap_value_label.text = f"{self.format_time(new_lap_time)}"
        self.speed_value_label.text = f"{self.SharedData.speed}"
        self.LV_value_label.text = f"{self.SharedData.lvvoltage}V"
        self.LV_value_label.color = (
            (1, 0, 0, 1) if self.SharedData.lvvoltage_low else (1, 1, 1, 1)
        )
        self.status_value_label.text = f"{self.SharedData.vcu_mode}"
        self.soc_value_label.text = f"{self.SharedData.orionsoc}%"

    def show_next_error_popup(self):
        """If there are pending error messages, show the next one in a popup."""
        if self.pending_error_messages and self.show_error:
            next_error = self.pending_error_messages.pop(0)
            self.error_popup = DismissablePopup(
                title="Critical Error Alert",
                content=Label(text=next_error, font_size="70sp", color=(1, 0, 0, 1)),
                size_hint=(0.8, 0.3),
            )
            self.error_popup.bind(on_dismiss=self.on_error_popup_dismiss)
            self.error_popup.open()
        pass

    def on_error_popup_dismiss(self, instance):
        self.error_popup = None
        # If there are more pending errors, show the next one.
        if self.pending_error_messages:
            self.show_next_error_popup()

    def generate_random_time(self):
        """Generate a random time in milliseconds between 10 and 180 seconds."""
        return random.randint(10000, 180000)

    def format_time(self, time_in_ms):
        """Format time into mm:ss:ms (minutes:seconds:milliseconds)."""
        minutes = time_in_ms // 60000
        seconds = (time_in_ms % 60000) // 1000
        milliseconds = time_in_ms % 1000
        return f"{minutes:02}:{seconds:02}:{milliseconds:03}"

    def _update_text_size(self, instance, value):
        # Set text_size to the width only so the text does not wrap vertically
        instance.text_size = (instance.width, None)


# Main App Class
class DashboardApp(App):
    def build(self):
        return Dash2()


if __name__ == "__main__":
    DashboardApp().run()
