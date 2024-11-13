import random
from itertools import count

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.progressbar import ProgressBar
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.graphics import Color, Rectangle, Ellipse, Line
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.screenmanager import Screen
from kivy.uix.scrollview import ScrollView
from screen_interface import ScreenInterface


# Main Dashboard Page
class DriverDashboard(Screen, ScreenInterface):  # Changed to inherit from Screen
    def __init__(self, **kwargs):
        super(DriverDashboard, self).__init__(**kwargs)
        super(DriverDashboard, self).__init__()
        self.orientation = 'horizontal'

        # Use a main BoxLayout to contain the dashboard elements
        main_layout = BoxLayout(orientation='horizontal')

        # Left section: Speed Display
        left_section = FloatLayout(size_hint=(0.6, 1))
        self.speed_label = Label(text='0 km/h', font_size='80sp', bold=True, color=(1, 1, 1, 1), size_hint=(1, 0.1), pos_hint={'x': -0.10, 'y': 0.48})
        left_section.add_widget(self.speed_label)
        main_layout.add_widget(left_section)

        # Right section using FloatLayout for precise widget positioning
        right_section = FloatLayout(size_hint=(0.4, 1))

        # Lap Times Label
        self.lap_times_label = Label(text='-----Lap Times----', font_size='22sp', bold=True, size_hint=(0.4, 0.1),
                                     pos_hint={'x': .15, 'y': 0.9})
        right_section.add_widget(self.lap_times_label)

        # ScrollView for Lap Times
        self.lap_times_box = BoxLayout(orientation='vertical', size_hint_y=None, height=290)
        self.lap_times = []  # Store the lap times
        for _ in range(5):
            label = Label(text='Lap 1: -- sec', font_size='27sp')
            self.lap_times.append(label)
            self.lap_times_box.add_widget(label)
        scroll_view = ScrollView(size_hint=(1.3, 0.3), pos_hint={'x': -0.3, 'y': 0.6})
        scroll_view.add_widget(self.lap_times_box)
        right_section.add_widget(scroll_view)

        # Battery SOC and Progress Bar
        self.soc_label = Label(text='Battery: 100%', font_size='22sp', size_hint=(0.4, 0.1),
                               pos_hint={'x': 0.05, 'y': 0.4})
        self.battery_bar = ProgressBar(max=100, value=100, size_hint=(0.8, 0.05), pos_hint={'x': 0.1, 'y': 0.35})
        right_section.add_widget(self.soc_label)
        right_section.add_widget(self.battery_bar)

        # Brake Pressure Display and Progress Bar
        self.brake_pressure_label = Label(text='Brake Pressure: kPa', font_size='20sp', size_hint=(0.4, 0.1),
                                          pos_hint={'x': 0.1, 'y': 0.25})
        self.brake_pressure_bar = ProgressBar(max=3000, value=0, size_hint=(0.8, 0.05), pos_hint={'x': 0.1, 'y': 0.2})
        right_section.add_widget(self.brake_pressure_label)
        right_section.add_widget(self.brake_pressure_bar)

        main_layout.add_widget(right_section)

        # Line across speed and Info
        with self.canvas:
            Color(1, 1, 1, 1)  # Set line color to red (RGBA format)
            Line(points=[870, 0, 870, 600], width=3)

        self.add_widget(main_layout)

        # Initialize simulation variables
        self.speed = 0
        self.soc = 100
        self.brake_pressure = 1
        self.lap_times_data = []  # Store simulated lap time data
        self.lap_energy = 0

        Clock.schedule_interval(self.update_simulation, 1)
        Clock.schedule_interval(self.display_random_fault, 10)

    # Update simulation with new random values
    def update_simulation(self, dt):
        # Update Speed (0 to 120 km/h)
        self.speed = random.randint(0, 120)
        self.speed_label.text = f'{self.speed} km/h'

        # Update Battery SOC (decreasing)
        self.soc = max(self.soc - random.randint(1, 5), 0)
        self.soc_label.text = f'Battery: {self.soc}%'
        self.battery_bar.value = self.soc

        # Update Brake Pressure (0 to 100%)
        self.brake_pressure = random.randint(0, 3000)
        self.brake_pressure_label.text = f'Brake Pressure: {self.brake_pressure}kPa'
        self.brake_pressure_bar.value = self.brake_pressure

        # Update Lap Times and Energy Data



        new_lap_time = random.randint(60, 180)  # Random lap time in seconds
        self.lap_energy = round(random.uniform(10, 50), 2)  # Random energy in kW
        lap = len(self.lap_times_data) + 1
        self.lap_times_data.append(f'Lap {lap}: {new_lap_time} sec | Energy: {self.lap_energy} kW')




        if len(self.lap_times_data) > 5:
            self.lap_times_data.pop(0)  # Keep the last 5 laps only

        for i, label in enumerate(self.lap_times):
            label.text = self.lap_times_data[i] if i < len(self.lap_times_data) else 'Lap 1: -- sec'




    # Display a random fault message
    def display_random_fault(self, dt):
        fault_messages = ['SDC Opened', 'TSAC Overheated', 'BOTS Triggered']
        random_fault = random.choice(fault_messages)
        fault_popup = Popup(title='Critical Fault',
                            content=Label(text=random_fault, font_size='40sp', color=(1, 0, 0, 1)),
                            size_hint=(0.6, 0.4))
        fault_popup.open()


# Main App Class
class DashboardApp(App):
    def build(self):
        Window.size = (1024, 600)  # Set a larger window size for better layout
        return DriverDashboard()


if __name__ == '__main__':
    DashboardApp().run()
