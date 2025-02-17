import random
import can
from kivy.app import App
import os
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.screenmanager import Screen
from kivy.core.window import Window
import canparser
from can_reader import subscribe_can_message
from can_reader import publish_message
from gui.pages.time_table_manager import TimeTableManager
from gui.widgets.custom_progress_bar import CustomProgressBar


# Main Dashboard Page
class DriverDashboard(Screen):
    def __init__(self, **kwargs):
        super(DriverDashboard, self).__init__(**kwargs)
        # Initialize Time Table Manager
        self.time_table_manager = TimeTableManager()
        # Can subs
        # Inverter
       # subscribe_can_message(canparser.MotorTemperatureData, self.update_motor_temp)
        subscribe_can_message(canparser.InverterTemperatureData, self.update_inverter_temp)
        #subscribe_can_message(canparser.InverterErrorsData, self.update_inverter_error)
      #  subscribe_can_message(canparser.VcuStateData, self.update_vcu_state)
        # Variables to update
        self.inverter_temp_value = 0
      #  self.update_inverter_error_state = False
      #  self.update_inverter_warning_state = False
      #  self.error = list
      #  self.warning = list
        #self.motor_temp_value = 0
        # Use a main FloatLayout to contain the dashboard elements, this allows for layering
        main_layout = FloatLayout()

        # Add a custom progress bar at the top of the screen
        self.top_progress_bar1 = CustomProgressBar(size_hint=(0.33, 0.1), pos_hint={'x': 0, 'y': 0.9},
                                                   threshold=0, max_value=40, default_color=(0, 1, 0, 1))
        self.top_progress_bar2 = CustomProgressBar(size_hint=(0.33, 0.1), pos_hint={'x': 0.33, 'y': 0.9},
                                                   threshold=40, max_value=80, default_color=(1, 0.65, 0, 1))
        self.top_progress_bar3 = CustomProgressBar(size_hint=(0.34, 0.1), pos_hint={'x': 0.66, 'y': 0.9},
                                                   threshold=80, max_value=120, default_color=(1, 0, 0, 1))
        main_layout.add_widget(self.top_progress_bar1)
        main_layout.add_widget(self.top_progress_bar2)
        main_layout.add_widget(self.top_progress_bar3)

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
                                         size_hint=(1, 0.1), pos_hint={'x': -0.05, 'y': 0.75})
        self.lapsleft_label = Label(text='Laps Left:', size_hint=(0.4, 0.1), pos_hint={'x': 0.03, 'y': 0.60}, font_size='35sp')
        self.lapsleftvalue_label = Label(text='0', size_hint=(0.2, 0.1), pos_hint={'x': 0.4, 'y': 0.60}, font_size='35sp')
        left_section.add_widget(self.last_lap_time_label)
        left_section.add_widget(self.lapsleft_label)
        left_section.add_widget(self.lapsleftvalue_label)

        # Speed Display
        self.speed_label = Label(text='0', font_size='80sp', bold=True, color=(1, 1, 1, 1), size_hint=(1, 0.1),
                                 pos_hint={'x': -0.10, 'y': 0.38})
        left_section.add_widget(self.speed_label)
        temps_layout = BoxLayout(orientation='horizontal', size_hint=(1.2, 0.2), pos_hint={'x': -0.3, 'y': 0.1})

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
        temps_layout.add_widget(inverter_box)
        left_section.add_widget(temps_layout)
        ui_layout.add_widget(left_section)

        # Right section using FloatLayout for precise widget positioning
        right_section = FloatLayout(size_hint=(0.4, 1), pos_hint={'x': 0.6, 'y': -0.2})

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
     #   self.lap_labels = []  # List of lap number labels (left column)
        self.time_labels = []  # List of time labels (middle column)
        self.energy_labels = []  # List of percentage/energy labels (right column)

        # Initialize lap counter
        self.lap_counter = 0  # Track total number of laps

        # Add empty labels initially (we will update them dynamically)
        for i in range(5):  # Showing up to 5 laps at a time
           # lap_label = Label(text=f"{i + 1}", font_size='22sp', color=(0, 1, 1, 1))
            time_label = Label(text="--:--:--", font_size='22sp', color=(1, 1, 1, 1))
            percent_label = Label(text="--", font_size='22sp', color=(1, 1, 1, 1))

#            self.lap_labels.append(lap_label)
            self.time_labels.append(time_label)
            self.energy_labels.append(percent_label)

#            lap_times_grid.add_widget(lap_label)
            lap_times_grid.add_widget(time_label)
            lap_times_grid.add_widget(percent_label)

        right_section.add_widget(lap_times_grid)

        # Battery SOC and Custom Progress Bar (loaded from custom_progress_bar.py)
        self.batter_label = Label(text='Battery:', font_size='29sp', size_hint=(0.4, 0.1), pos_hint={'x': -0.35, 'y': 0.4})
        self.soc_label = Label(text='100%', font_size='29sp', size_hint=(0.4, 0.1),
                               pos_hint={'x': -0.15, 'y': 0.4})
        self.avgenergy_label = Label(text='Average Energy Used:', font_size='15sp', size_hint=(0.4, 0.1), pos_hint={'x': 0.1, 'y': 0.4})
        self.avgenergyprocent_label = Label(text='0%', size_hint=(0.4, 0.1), pos_hint={'x': 0.3, 'y': 0.4})



        # Instantiate CustomProgressBar with intervals enabled and custom thresholds
        self.custom_battery_bar = CustomProgressBar(
            size_hint=(1.3, 0.05),
            pos_hint={'x': -0.29, 'y': 0.35},
            green_threshold=50,  # Green above 50%
            orange_threshold=30,  # Orange below 30%
            intervals=True  # Enable color intervals
        )
        right_section.add_widget(self.batter_label)
        right_section.add_widget(self.soc_label)
        right_section.add_widget(self.custom_battery_bar)
        right_section.add_widget(self.avgenergy_label)
        right_section.add_widget(self.avgenergyprocent_label)


        # If you want to add Cooling loop temp later on.


      #  # Cool Loop Temp Section (Left)
      #  cool_loop_box = BoxLayout(orientation='vertical')
      #  self.cool_loop_label = Label(
      #      text="COOL LOOP TEMP",
     #       font_size='25sp',
     #       color=(0, 1, 1, 1),
     #       halign='center'
     #   )
     #   self.cool_loop_temp = Label(
     #       text="000 C",
     #       font_size='30sp',
     #       color=(1, 1, 1, 1),
     #       halign='center'
     #   )
     #   cool_loop_box.add_widget(self.cool_loop_label)
      #  cool_loop_box.add_widget(self.cool_loop_temp)

        # Inverter Temp Section (Right)


        # Add Cool Loop and Inverter Boxes to the layout
        #temps_layout.add_widget(cool_loop_box)



        ui_layout.add_widget(right_section)

        # Add the UI layout on top of the logo background
        main_layout.add_widget(ui_layout)

        self.add_widget(main_layout)

        # Initialize simulation variables
        self.speed = 0
        self.soc = 100  # Track remaining SOC
        self.last_soc = 100  # Track SOC at the start of the lap

        # Define temperature thresholds for color change
        self.cooling_temp_threshold_low = 30
        self.cooling_temp_threshold_high = 70
        self.inverter_temp_threshold_high = 70

    # Using refresh to refresh the screen values.

    def refresh(self):

        # Update speed
        self.speed = random.randint(0, 120)
        self.speed_label.text = f'{self.speed}'
        # Update speed bar
        self.top_progress_bar1.set_value(self.speed)
        self.top_progress_bar2.set_value(self.speed)
        self.top_progress_bar3.set_value(self.speed)
        # Update battery SOC
        new_soc = max(self.soc - random.randint(1, 5), 0)
        soc_used = self.last_soc - new_soc  # Calculate SOC used for the lap
        self.last_soc = new_soc  # Update last SOC for next lap calculation
        self.soc = new_soc  # Update remaining SOC
        self.soc_label.text = f'{self.soc}%'  # Update label with battery percentage
        self.custom_battery_bar.set_value(self.soc)  # Update custom progress bar
        self.avgeng(self.time_table_manager.energy_data, self.time_table_manager.lap_times)

        # Simulate new temperature values between 22 and 100°C
        #cool_loop_temp_value = random.randint(22, 100)
        #inverter_temp_value = random.randint(22, 100)
       # self.cool_loop_temp.text = f"{cool_loop_temp_value} C"
        self.inverter_temp.text = f"{self.inverter_temp_value} C"

        # Check if cooling loop temperature is within the threshold and change the color dynamically
       # if cool_loop_temp_value > self.cooling_temp_threshold_high:
            #self.cool_loop_temp.color = (1, 0, 0, 1)  # Red if temperature is below or above threshold
       # else:
           # self.cool_loop_temp.color = (1, 1, 1, 1)

      #  if self.inverter_temp_value > self.inverter_temp_threshold_high:
     #       self.inverter_temp.color = (1, 0, 0, 1)
     #   else:
      #      self.inverter_temp.color = (1, 1, 1, 1)

        # Check battery SOC to change the colour

        if self.soc < 30:
            self.soc_label.color = (1, 0, 0, 1)

        # Simulate new lap time and energy consumption
        self.lap_counter += 1  # Increment the total lap count
        new_lap_time = self.generate_random_time()

        # Add the new lap time and SOC used to the time table manager
        best_lap, all_time_best_lap, lap_times, energy_data = self.time_table_manager.add_lap_time(new_lap_time, soc_used)

        # Update the lap display labels
       # self.time_table_manager.update_lap_display(self.lap_labels, self.time_labels, self.energy_labels)

        # Update the "BEST LAP" label to display the all-time best lap
        if all_time_best_lap:
            self.bestlap_time_label.text = f'{self.time_table_manager.format_time(all_time_best_lap)}'

        # Update last lap comparison (green/yellow)
        last_lap_color = self.time_table_manager.compare_last_lap(new_lap_time)
        print(last_lap_color)
        self.last_lap_time_label.color = (0, 1, 0, 1) if last_lap_color == 'green' else (1, 1, 0, 1)
        self.last_lap_time_label.text = f'Last Lap: {self.format_time(new_lap_time)}'
        publish_message(can.Message(arbitration_id=0x181, data=[0x49, 0x13, 0x25, 0x00]))

    # Inverter Update Section
   # def update_inverter_error(self, message:canparser.InverterErrorsData):
   #     self.update_inverter_error_state = bool(message.has_error)
   #     self.update_inverter_warning_state = bool(message.has_warning)
   #     self.error = list(message.decoded_errors)
   #     self.warning = list(message.decoded_warnings)
    def update_inverter_temp(self, message):
       self.inverter_temp_value = round(message.parsed_data.temperature_c)
  #  def update_motor_temp(self, message):
  #      self.motor_temp_value = round(message.parsed_data.temperature_c)
    # Vcu update Section
   # def update_vcu(self, message:canparser.VcuStateData):
   #     self.update_vcu_state = bool(message.canparser.VcuStateData)


    # BTMU Update section

   # def update_soc(self, message):
   #     self.soc = round(message.parsed_data.)
   # def bat_temp(self, message):
    #    self.bat_temp_value = round(message.parsed_data.)

    def avgeng(self, energy_data, lap_times):
        englap = 0
        lapsleft = 0
        if len(lap_times) == 0 and len(energy_data) == 0 and englap == 0 and lapsleft == 0:
            return
        else:
            englap = round(sum(energy_data) / len(lap_times), 1)
            if englap == 0:
                return
            lapsleft = round(self.soc / englap)
            self.avgenergyprocent_label.text = f'{englap}%'
            self.lapsleftvalue_label.text = f'{lapsleft}'


   # def avg_energy_left(self, lap_times, energy_data, soc):
      #  avgeng = (sum(energy_data) / len(lap_times))
      #  lapsleft = soc / avgeng  ## fixa SOC från dashboard.
      #  return print(float(lapsleft))

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
