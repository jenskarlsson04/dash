import random
from kivy.app import App
import os
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.screenmanager import Screen
from kivy.core.window import Window
from kivy.clock import Clock

# Import TimeTableManager
from Pages.time_table_manager import TimeTableManager

# Import the custom progress bar from the custom_progress_bar.py file
from Pages.custom_progress_bar import CustomProgressBar

# Main Dashboard Page
class DriverDashboard(Screen):
    def __init__(self, **kwargs):
        super(DriverDashboard, self).__init__(**kwargs)
        self.orientation = 'horizontal'

        # Initialize Time Table Manager
        self.time_table_manager = TimeTableManager()

        # Use a main FloatLayout to contain the dashboard elements, this allows for layering
        main_layout = FloatLayout()
        image_path = os.path.join('./images/logo.png')

        # Add the background logo (logo.png) with low opacity
        self.logo_image = Image(
            source=image_path,
            opacity=0.15,
            allow_stretch=True,
            keep_ratio=True,
            size_hint=(0.6, 0.6),  # Half the width and height of the screen
            pos_hint={'center_x': 0.5, 'center_y': 0.5}  # Center the image
        )
        main_layout.add_widget(self.logo_image)

        # Use a BoxLayout for the actual dashboard UI
        ui_layout = BoxLayout(orientation='horizontal', size_hint=(1, 1))

        # Left section: Speed Display
        left_section = FloatLayout(size_hint=(0.6, 1))

        # Last Lap Time Label (Dynamic Color: Green or Yellow)
        self.last_lap_time_label = Label(text='Last Lap: --:--:--', font_size='35sp', bold=True, color=(1, 1, 1, 1),
                                         size_hint=(1, 0.1), pos_hint={'x': -0.05, 'y': 0.85})
        left_section.add_widget(self.last_lap_time_label)

        # Speed Display
        self.speed_label = Label(text='0 km/h', font_size='80sp', bold=True, color=(1, 1, 1, 1), size_hint=(1, 0.1),
                                 pos_hint={'x': -0.10, 'y': 0.48})
        left_section.add_widget(self.speed_label)
        ui_layout.add_widget(left_section)

        # Right section using FloatLayout for precise widget positioning
        right_section = FloatLayout(size_hint=(0.4, 1))

        # Lap Times Layout (BEST LAP and Lap Data)
        self.bestlap_label = Label(text='BEST LAP:', font_size='24sp', bold=True, color=(0, 1, 1, 1),
                                   size_hint=(0.2, 0.05), pos_hint={'x': 0.18, 'y': 0.87})
        self.bestlap_time_label = Label(text='--:--:--', font_size='24sp', bold=False, color=(1, 0, 1, 1),
                                        size_hint=(0.4, 0.05), pos_hint={'x': 0.38, 'y': 0.869})
        right_section.add_widget(self.bestlap_label)
        right_section.add_widget(self.bestlap_time_label)

        # Lap Times Grid Layout for all lap information
        lap_times_grid = GridLayout(cols=3, spacing=10, size_hint=(0.9, 0.3), pos_hint={'x': 0.05, 'y': 0.5})

        # Add headers
        lap_times_grid.add_widget(Label(text='Lap', font_size='20sp', bold=True, color=(0, 1, 1, 1)))
        lap_times_grid.add_widget(Label(text='Time', font_size='20sp', bold=True, color=(1, 1, 1, 1)))
        lap_times_grid.add_widget(Label(text='% Used', font_size='20sp', bold=True, color=(1, 1, 1, 1)))

        # Create Lap Time Labels
        self.lap_labels = []  # List of lap number labels (left column)
        self.time_labels = []  # List of time labels (middle column)
        self.energy_labels = []  # List of percentage/energy labels (right column)

        # Initialize lap counter
        self.lap_counter = 0  # Track total number of laps

        # Add empty labels initially (we will update them dynamically)
        for i in range(5):  # Showing up to 5 laps at a time
            lap_label = Label(text=f"{i + 1}", font_size='22sp', color=(0, 1, 1, 1))
            time_label = Label(text="--:--:--", font_size='22sp', color=(1, 1, 1, 1))
            percent_label = Label(text="--", font_size='22sp', color=(1, 1, 1, 1))

            self.lap_labels.append(lap_label)
            self.time_labels.append(time_label)
            self.energy_labels.append(percent_label)

            lap_times_grid.add_widget(lap_label)
            lap_times_grid.add_widget(time_label)
            lap_times_grid.add_widget(percent_label)

        right_section.add_widget(lap_times_grid)

        # Battery SOC and Custom Progress Bar (loaded from custom_progress_bar.py)
        self.soc_label = Label(text='Battery: 100%', font_size='29sp', size_hint=(0.4, 0.1),
                               pos_hint={'x': -0.25, 'y': 0.4})

        # Instantiate CustomProgressBar with intervals enabled and custom thresholds
        self.custom_battery_bar = CustomProgressBar(
            size_hint=(1.3, 0.05),
            pos_hint={'x': -0.29, 'y': 0.35},
            green_threshold=50,  # Green above 50%
            orange_threshold=30,  # Orange below 30%
            intervals=True  # Enable color intervals
        )
        right_section.add_widget(self.soc_label)
        right_section.add_widget(self.custom_battery_bar)

        # Cooling loop temp and Inverter temp sections
        temps_layout = BoxLayout(orientation='horizontal', size_hint=(1.2, 0.15), pos_hint={'x': -0.3, 'y': 0.15})

        # Cool Loop Temp Section (Left)
        cool_loop_box = BoxLayout(orientation='vertical')
        self.cool_loop_label = Label(
            text="COOL LOOP TEMP",
            font_size='25sp',
            color=(0, 1, 1, 1),
            halign='center'
        )
        self.cool_loop_temp = Label(
            text="000 C",
            font_size='30sp',
            color=(1, 1, 1, 1),
            halign='center'
        )
        cool_loop_box.add_widget(self.cool_loop_label)
        cool_loop_box.add_widget(self.cool_loop_temp)

        # Inverter Temp Section (Right)
        inverter_box = BoxLayout(orientation='vertical')
        self.inverter_label = Label(
            text="INVERTER TEMP",
            font_size='25sp',
            color=(0, 1, 1, 1),
            halign='center'
        )
        self.inverter_temp = Label(
            text="000 C",
            font_size='30sp',
            color=(1, 1, 1, 1),
            halign='center'
        )
        inverter_box.add_widget(self.inverter_label)
        inverter_box.add_widget(self.inverter_temp)

        # Add Cool Loop and Inverter Boxes to the layout
        temps_layout.add_widget(cool_loop_box)
        temps_layout.add_widget(inverter_box)

        right_section.add_widget(temps_layout)
        ui_layout.add_widget(right_section)

        # Add the UI layout on top of the logo background
        main_layout.add_widget(ui_layout)

        # Line across speed and Info
       # with self.canvas:
        #    Color(1, 1, 1, 1)  # Set line color to white (RGBA format)
        #    Line(points=[870, 0, 870, 600], width=3)

        self.add_widget(main_layout)

        # Initialize simulation variables
        self.speed = 0
        self.soc = 100  # Track remaining SOC
        self.last_soc = 100  # Track SOC at the start of the lap
        self.brake_pressure = 1

        # ---- Updating the values randomly ----
        Clock.schedule_interval(self.update_screen, 0.5)

    def update_screen(self, data_type=None):
        # Update speed
        self.speed = random.randint(0, 120)
        self.speed_label.text = f'{self.speed} km/h'

        # Update battery SOC
        new_soc = max(self.soc - random.randint(1, 5), 0)
        soc_used = self.last_soc - new_soc  # Calculate SOC used for the lap
        self.last_soc = new_soc  # Update last SOC for next lap calculation
        self.soc = new_soc  # Update remaining SOC
        self.soc_label.text = f'Battery: {self.soc}%'  # Update label with battery percentage
        self.custom_battery_bar.set_value(self.soc)  # Update custom progress bar

        # Simulate new temperature values between 22 and 100°C
        cool_loop_temp_value = random.randint(22, 100)
        inverter_temp_value = random.randint(22, 100)
        self.cool_loop_temp.text = f"{cool_loop_temp_value} C"
        self.inverter_temp.text = f"{inverter_temp_value} C"

        # Simulate new lap time and energy consumption
        self.lap_counter += 1  # Increment the total lap count
        new_lap_time = self.generate_random_time()

        # Add the new lap time and SOC used to the time table manager
        best_lap, all_time_best_lap, lap_times, energy_data = self.time_table_manager.add_lap_time(new_lap_time, soc_used)

        # Update the lap display labels
        self.time_table_manager.update_lap_display(self.lap_labels, self.time_labels, self.energy_labels)

        # Update the "BEST LAP" label to display the all-time best lap
        if all_time_best_lap:
            self.bestlap_time_label.text = f'{self.time_table_manager.format_time(all_time_best_lap)}'

        # Update last lap comparison (green/yellow)
        last_lap_color = self.time_table_manager.compare_last_lap(new_lap_time)
        self.last_lap_time_label.color = (0, 1, 0, 1) if last_lap_color == 'green' else (1, 1, 0, 1)
        self.last_lap_time_label.text = f'Last Lap: {self.format_time(new_lap_time)}'

    def format_time(self, time_in_ms):
        # Format time into mm:ss:ms (minutes:seconds:milliseconds)
        minutes = time_in_ms // 60000
        seconds = (time_in_ms % 60000) // 1000
        milliseconds = time_in_ms % 1000
        return f"{minutes:02}:{seconds:02}:{milliseconds:03}"

    def generate_random_time(self):
        # Generate a random time in milliseconds between 10 and 180 seconds (i.e., 10000 ms to 180000 ms)
        return random.randint(10000, 180000)



# Main App Class
class DashboardApp(App):
    def build(self):
        Window.size = (1024, 600)  # Set a larger window size for better layout
        return DriverDashboard()

if __name__ == '__main__':
    DashboardApp().run()
