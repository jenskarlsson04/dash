import random
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.progressbar import ProgressBar
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.scrollview import ScrollView

# Main Dashboard Page
class DriverDashboard(BoxLayout):
    def __init__(self, **kwargs):
        super(DriverDashboard, self).__init__(**kwargs)
        self.orientation = 'horizontal'

        # Left section: Speed Display
        left_section = BoxLayout(orientation='vertical', size_hint=(0.6, 1))
        self.speed_label = Label(text='Speed: 0 km/h', font_size='80sp', bold=True, color=(1, 1, 1, 1))
        left_section.add_widget(self.speed_label)
        self.add_widget(left_section)

        # Right section: Lap Times, SOC, Brake Pressure, and Messages
        right_section = GridLayout(cols=1, size_hint=(0.4, 1), spacing=20, padding=10)

        # Lap Times List
        self.lap_times_label = Label(text='Lap Times:', font_size='30sp', bold=True)
        right_section.add_widget(self.lap_times_label)

        self.lap_times_box = BoxLayout(orientation='vertical', size_hint_y=None, height=200)
        self.lap_times = []  # Store the lap times
        for _ in range(5):
            label = Label(text='Lap: -- sec', font_size='20sp')
            self.lap_times.append(label)
            self.lap_times_box.add_widget(label)
        scroll_view = ScrollView(size_hint=(1, None), size=(Window.width * 0.4, 200))
        scroll_view.add_widget(self.lap_times_box)
        right_section.add_widget(scroll_view)

        # Battery SOC and Progress Bar
        self.soc_label = Label(text='Battery SOC: 100%', font_size='20sp')
        right_section.add_widget(self.soc_label)
        self.battery_bar = ProgressBar(max=100, value=100)
        right_section.add_widget(self.battery_bar)


        # Brake Pressure Display and Progress Bar
        self.brake_pressure_label = Label(text='Brake Pressure: kPa', font_size='20sp')
        right_section.add_widget(self.brake_pressure_label)
        self.brake_pressure_bar = ProgressBar(max=3000, value=0)
        right_section.add_widget(self.brake_pressure_bar)

        self.add_widget(right_section)

        # Initialize simulation variables
        self.speed = 0
        self.soc = 100
        self.brake_pressure = 1
        self.lap_times_data = []  # Store simulated lap time data
        self.lap_energy = 0

    def on_enter(self):
        # Start the clock when entering the screen
        print("Start")
        self.clock_event = Clock.schedule_interval(self.update_simulation, 1)
        self.clock_event2 = Clock.schedule_interval(self.display_random_fault, 10)

    def on_leave(self):
        # Stop the clock when leaving the screen
        if self.clock_event:
            self.clock_event.cancel()
            self.clock_event2.cancel()


    # Update simulation with new random values
    def update_simulation(self, dt):
        # Update Speed (0 to 120 km/h)
        self.speed = random.randint(0, 120)
        self.speed_label.text = f'Speed: {self.speed} km/h'

        # Update Battery SOC (decreasing)
        self.soc = max(self.soc - random.randint(1, 5), 0)
        self.soc_label.text = f'Battery SOC: {self.soc}%'
        self.battery_bar.value = self.soc

        # Update Brake Pressure (0 to 100%)
        self.brake_pressure = random.randint(0, 3000)
        self.brake_pressure_label.text = f'Brake Pressure: {self.brake_pressure}kPa'
        self.brake_pressure_bar.value = self.brake_pressure

        # Change bar color based on pressure values
        if self.brake_pressure < 30:
            self.brake_pressure_bar.color = [0, 1, 0, 1]  # Green
        elif self.brake_pressure < 60:
            self.brake_pressure_bar.color = [1, 1, 0, 1]  # Yellow
        else:
            self.brake_pressure_bar.color = [1, 0, 0, 1]  # Red

        # Update Lap Times and Energy Data
        new_lap_time = random.randint(60, 180)  # Random lap time in seconds
        self.lap_energy = round(random.uniform(10, 50), 2)  # Random energy in kW

        # Update lap times display with a rolling list of 5 laps
        self.lap_times_data.append(f'Lap: {new_lap_time} sec | Energy: {self.lap_energy} kW')
        if len(self.lap_times_data) > 5:
            self.lap_times_data.pop(0)  # Keep the last 5 laps only

        # Update the labels
        for i, label in enumerate(self.lap_times):
            if i < len(self.lap_times_data):
                label.text = self.lap_times_data[i]
            else:
                label.text = 'Lap: -- sec'

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
        Window.size = (1200, 600)  # Set a larger window size for better layout
        return DriverDashboard()


