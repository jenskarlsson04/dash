import random
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import Screen
from kivy.core.window import Window
from gui.pages.time_table_manager import TimeTableManager
from gui.widgets.custom_progress_bar import CustomProgressBar
from gui.widgets.BatteryWidget import BatteryWidget
from gui.widgets.Statusbar import Statusbar

# Main Dashboard Page
class Dash(Screen):
    def __init__(self, **kwargs):
        super(Dash, self).__init__(**kwargs)
        # Initialize Time Table Manager
        self.time_table_manager = TimeTableManager(total_laps=22)

        # Can subscriptions



        # Variables to update
        self.inverter_temp_value = 0
        self.soc = 100  # Track remaining SOC
        self.last_soc = 100  # Track SOC at the start of the lap
        self.lap_counter = 0  # Track total number of laps
        self.error = False # looks for error, if no error dont make place for message window
        self.canisup = False # Sets CAN as up
        self.batterythreshold = 4.55 # % 4.55% per lap for 22 laps covvage.
        self.laps = 22

        # Use a main FloatLayout to contain the dashboard elements
        main_layout = FloatLayout()

        # Add a custom progress bar at the top of the screen
        self.top_progress_bar1 = CustomProgressBar(size_hint=(0.33, 0.2), pos_hint={'x': 0, 'y': 0.8},
                                                   threshold=0, max_value=40, default_color=(0, 1, 0, 1))
        self.top_progress_bar2 = CustomProgressBar(size_hint=(0.33, 0.2), pos_hint={'x': 0.33, 'y': 0.8},
                                                   threshold=40, max_value=80, default_color=(1, 0.65, 0, 1))
        self.top_progress_bar3 = CustomProgressBar(size_hint=(0.34, 0.2), pos_hint={'x': 0.66, 'y': 0.8},
                                                   threshold=80, max_value=120, default_color=(1, 0, 0, 1))
        main_layout.add_widget(self.top_progress_bar1)
        main_layout.add_widget(self.top_progress_bar2)
        main_layout.add_widget(self.top_progress_bar3)


        # Add the background logo (logo.png) with low opacity
       # image_path = os.path.join('./images/logo.png')
      #  self.logo_image = Image(
      #      source=image_path,
     #       opacity=0.15,
     #       allow_stretch=True,
     #       keep_ratio=True,
      #      size_hint=(0.6, 0.6),  # Half the width and height of the screen
     #       pos_hint={'center_x': 0.5, 'center_y': 0.5}  # Center the image
       # )
      #  main_layout.add_widget(self.logo_image)

        # Use a BoxLayout for the actual dashboard UI Uppdatera för att inte ha left section!!
        ui_layout = BoxLayout(orientation='horizontal', size_hint=(1, 1))

        left_section = FloatLayout(size_hint=(0.6, 1))
        self.last_lap_time_label = Label(text='Last Lap: --:--:--', font_size='70sp', bold=True, color=(1, 1, 1, 1),
                                         size_hint=(1, 0), pos_hint={'x': 0, 'y': 0.68})
        left_section.add_widget(self.last_lap_time_label)
        ui_layout.add_widget(left_section)

        # Add the battery symbol widget
        if not self.error:  # Introducing the possibility to move the icon when a error is displayed.
            self.battery_widget = BatteryWidget(size_hint=(0.3, 0.2), pos_hint={'x': 0.35, 'y': 0.35})
            main_layout.add_widget(self.battery_widget)

        # Battery threshold

        self.batterythreshold_label = Label(text='', font_size='60sp', bold=True, color=(1, 0, 0, 1),
                                      size_hint=(1, 0), pos_hint={'x': 0, 'y': 0.22})
        main_layout.add_widget(self.batterythreshold_label)

        # Add the status bar
        self.status_bar = Statusbar(size_hint=(1, None), height=100, pos_hint={'x': 0, 'y': 0})
        main_layout.add_widget(self.status_bar)
        self.canup()

        # Add the UI layout on top of the logo background
        main_layout.add_widget(ui_layout)

        self.add_widget(main_layout)

    def refresh(self):
        """Refresh the dashboard values."""
        # Update speed
        #self.speed = 120
        self.speed = random.randint(0, 120)
        self.top_progress_bar1.set_value(self.speed)
        self.top_progress_bar2.set_value(self.speed)
        self.top_progress_bar3.set_value(self.speed)

        # Update last lap time
        new_lap_time = self.generate_random_time()
        result = self.time_table_manager.add_lap_time(new_lap_time)
        last_lap_color = self.time_table_manager.compare_last_lap(new_lap_time)
        self.last_lap_time_label.color = (0, 1, 0, 1) if last_lap_color == 'green' else (1, 0.85, 0, 1)
        self.last_lap_time_label.text = f'Last Lap: {self.format_time(new_lap_time)}'

        # Simulate battery SOC
        #print(result['laps_remaining'])
       # print(result['required_soc'])
        self.soc = max(self.soc - random.randint(1, 10), 0)

        # Update battery color based on SOC
        if not result['sufficient_soc']:
            self.batterythreshold_label.text = 'Below Threshold'
            self.battery_widget.update_color("red")
        else:
            self.battery_widget.update_color("green")
            self.batterythreshold_label.text = ''



        # Change bar if car is down/up.
    def canup(self):
        if self.canisup:
            self.status_bar.status = True
        else:
            self.status_bar.status = False

    def format_time(self, time_in_ms):
        """Format time into mm:ss:ms (minutes:seconds:milliseconds)."""
        minutes = time_in_ms // 60000
        seconds = (time_in_ms % 60000) // 1000
        milliseconds = time_in_ms % 1000
        return f"{minutes:02}:{seconds:02}:{milliseconds:03}"

    def generate_random_time(self):
        """Generate a random time in milliseconds between 10 and 180 seconds."""
        return random.randint(10000, 180000)


# Main App Class
class DashboardApp(App):
    def build(self):
        Window.size = (1024, 600)  # Set a larger window size for better layout
        return Dash()


if __name__ == '__main__':
    DashboardApp().run()
