from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.properties import NumericProperty
from kivy.uix.progressbar import ProgressBar
import random


# Main Dashboard Class (inherits BoxLayout)
class Dashboard(BoxLayout):
    # Numeric properties to track live data
    speed = NumericProperty(0)
    fuel = NumericProperty(100)  # Start with a full tank
    engine_temp = NumericProperty(70)  # Normal engine temp

    def __init__(self, **kwargs):
        super(Dashboard, self).__init__(**kwargs)

        # Set orientation of the layout
        self.orientation = 'vertical'
        self.padding = 20
        self.spacing = 20

        # Create a speed section
        speed_layout = BoxLayout(orientation='horizontal')
        speed_label = Label(text="Speed:", font_size=32)
        self.speed_value_label = Label(text=f"{self.speed} km/h", font_size=48, color=(1, 0, 0, 1))  # Red text
        speed_layout.add_widget(speed_label)
        speed_layout.add_widget(self.speed_value_label)

        # Create a fuel section with progress bar
        fuel_layout = BoxLayout(orientation='horizontal')
        fuel_label = Label(text="Fuel Level:", font_size=32)
        self.fuel_bar = ProgressBar(max=100, value=self.fuel, size_hint=(1, 0.2))  # Fuel ProgressBar
        self.fuel_value_label = Label(text=f"{self.fuel:.0f} %", font_size=48)  # Fuel percentage
        fuel_layout.add_widget(fuel_label)
        fuel_layout.add_widget(self.fuel_bar)
        fuel_layout.add_widget(self.fuel_value_label)

        # Create an engine temperature section
        temp_layout = BoxLayout(orientation='horizontal')
        temp_label = Label(text="Engine Temp:", font_size=32)
        self.temp_value_label = Label(text=f"{self.engine_temp} °C", font_size=48, color=(0, 0, 1, 1))  # Blue text
        temp_layout.add_widget(temp_label)
        temp_layout.add_widget(self.temp_value_label)

        # Add all layouts to the main dashboard
        self.add_widget(speed_layout)
        self.add_widget(fuel_layout)
        self.add_widget(temp_layout)

        # Schedule the update of the dashboard every 0.5 seconds (simulating live data)
        Clock.schedule_interval(self.update_dashboard, 0.016)

    def update_dashboard(self, dt):
        """
        Simulate and update live data for speed, fuel, and engine temperature.
        """
        # Simulate random speed changes
        self.speed = random.randint(0, 200)  # Speed in km/h
        self.speed_value_label.text = f"{self.speed:.0f} km/h"

        # Simulate fuel consumption over time
        self.fuel = max(0, self.fuel - random.uniform(0.1, 1.0))  # Decrease fuel, no negative values
        self.fuel_bar.value = self.fuel
        self.fuel_value_label.text = f"{self.fuel:.0f} %"

        # Simulate engine temperature variation
        self.engine_temp = random.randint(70, 120)  # Temperature in degrees Celsius
        self.temp_value_label.text = f"{self.engine_temp} °C"