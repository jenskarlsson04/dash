import os

# Import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import Screen
from kivy.graphics import Color, Line
from kivy.uix.image import Image
from kivy.core.window import Window

from GPIO_reader import btn_lap
from GPIO_reader.gpio_class import btn_reset
# Import lap time handler

# Import Custom widgets
from gui.widgets import OutlinedBox
from gui.shared_data import SharedDataDriver

#Import gpio for reset
from GPIO_reader.gpio_subscription import subscribe_gpio_pint


# Import data
from FileSave import SaveToFile, PERSISTENT_FILENAME, STATS_FILENAME


# Main Dashboard Page
class Afterdrive(Screen):
    def __init__(self, **kwargs):
        super(Afterdrive, self).__init__(**kwargs)

        self.shared_data = SharedDataDriver()

        self.stats_current = SaveToFile(STATS_FILENAME)
        self.stats_pres = SaveToFile(PERSISTENT_FILENAME)

        self.presistant_stats = self.stats_pres.load()
        self.current_stats = self.stats_current.load() #Uppdateras dessa helatiden efter att den har loadats???
        subscribe_gpio_pint(btn_reset, self.reset_file)

        # Use a main layout to contain the dashboard elements




        # Huvudlayout: Vertikal BoxLayout med header, separator och innehåll

        main_layout = BoxLayout(orientation="vertical", padding=10, spacing=10)

        # 1. HEADER (Debug - Logo - Orion)
        header_layout = BoxLayout(orientation="horizontal", size_hint=(1, 0.15))
        self.debug_label = Label(
            text="Race",
            font_size="70sp",
            size_hint_x=0.3,
            color=(0, 1, 1, 1),
            halign="left",
            valign="middle",
        )

        # ADD A TEXT AND VALUE INSTEAD

        # REMOVED FOR VALUE INSTEAD
        image_path = os.path.join("./gui/images/logo.png")
        self.logo_image = Image(
            source=image_path,
            opacity=0.15,
            allow_stretch=True,
            keep_ratio=True,
            size_hint_x=0.4,
        )

        self.stats_label = Label(
            text="Stats",
            font_size="70sp",
            size_hint_x=0.3,
            color=(0, 1, 1, 1),
            halign="right",
            valign="middle",
        )
        header_layout.add_widget(self.debug_label)
        header_layout.add_widget(self.logo_image)
        header_layout.add_widget(self.stats_label)

        # 2. SEPARATOR (Linje direkt under headern) - integrated here
        separator = Widget(size_hint=(1, None), height=5)
        with separator.canvas:
            Color(1, 1, 2, 0.5)
            self.separator_line = Line(points=[], width=8)
        separator.bind(pos=self._update_separator, size=self._update_separator)

        # 3. CONTENT
        content_layout = BoxLayout(
            orientation="horizontal", spacing=10, size_hint=(1, 0.85)
        )

        # Vänster innehåll
        middle_content = OutlinedBox(
            orientation="vertical", spacing=10, size_hint=(0.33, 1)
        )

        speed_max_container = BoxLayout(
            orientation="vertical", spacing=5, size_hint=(1, 0.2)
        )  # change #1
        self.speed_max_text_label = Label(  # 2
            text="Speed Max",
            font_size="40sp",
            halign="left",
            valign="middle",
            size_hint=(1, 0.2),
            color=(0, 1, 1, 1),
        )
        self.speed_max_text_label.bind(size=self._update_text_size)  # change to #2
        speed_max_container.add_widget(self.speed_max_text_label)  # change to #1 and #2

        speed_max_value = BoxLayout(orientation="horizontal", size_hint=(1, 0.2))  # 3
        self.speed_max_value_label = Label(  # change to #3, #4
            text="000",
            font_size="45sp",
            halign="left",
            valign="middle",
            size_hint_x=0.7,
            width=160,
            color=(1, 1, 1, 1),
        )
        self.speed_max_value_label.bind(size=self._update_text_size)  # change to #4
        speed_max_value.add_widget(self.speed_max_value_label)
        self.speed_max_unit_label = Label(
            text="kmh",
            font_size="45sp",
            halign="left",
            valign="middle",
            size_hint_x=2,
            width=60,
            color=(1, 1, 1, 1),
        )
        self.speed_max_unit_label.bind(size=self._update_text_size)
        speed_max_value.add_widget(self.speed_max_unit_label)
        speed_max_container.add_widget(speed_max_value)
        middle_content.add_widget(speed_max_container)

        lv_bat_voltage_min_container = BoxLayout(
            orientation="vertical", spacing=5, size_hint=(1, 0.2)
        )  # change #1
        self.lv_bat_low_text_label = Label(  # 2
            text="LV Voltage Min",
            font_size="40sp",
            halign="left",
            valign="middle",
            size_hint=(1, 0.4),
            color=(0, 1, 1, 1),
        )
        self.lv_bat_low_text_label.bind(size=self._update_text_size)  # change to #2
        lv_bat_voltage_min_container.add_widget(
            self.lv_bat_low_text_label
        )  # change to #1 and #2

        lv_bat_low_value_layout = BoxLayout(
            orientation="horizontal", size_hint=(1, 0.6), spacing=5
        )  # 3
        self.lv_bat_low_value_label = Label(  # change to #3, #4
            text="000",
            font_size="45sp",
            halign="left",
            valign="middle",
            size_hint_x=0.7,
            width=160,
            color=(1, 1, 1, 1),
        )
        self.lv_bat_low_value_label.bind(size=self._update_text_size)  # change to #4
        lv_bat_low_value_layout.add_widget(self.lv_bat_low_value_label)
        self.lv_bat_unit_label = Label(
            text="V",
            font_size="45sp",
            halign="left",
            valign="middle",
            size_hint_x=2,
            width=80,
            color=(1, 1, 1, 1),
        )
        self.lv_bat_unit_label.bind(size=self._update_text_size)
        lv_bat_low_value_layout.add_widget(self.lv_bat_unit_label)
        lv_bat_voltage_min_container.add_widget(lv_bat_low_value_layout)

        middle_content.add_widget(lv_bat_voltage_min_container)

        # Motor Temperature-container
        total_driving_time_container = BoxLayout(
            orientation="vertical", spacing=5, size_hint=(1, 0.2)
        )
        self.total_driving_time_text_label = Label(
            text="Total Driving Time",
            font_size="40sp",
            halign="left",
            valign="middle",
            size_hint=(1, 0.4),
            color=(0, 1, 1, 1),
        )
        self.total_driving_time_text_label.bind(size=self._update_text_size)
        total_driving_time_container.add_widget(self.total_driving_time_text_label)

        total_driving_time_layout = BoxLayout(
            orientation="horizontal", size_hint=(1, 0.6), spacing=5
        )
        self.total_driving_time_label = Label(
            text="N/A",
            font_size="45sp",
            halign="left",
            valign="middle",
            size_hint_x=0.3,
            width=160,
            color=(1, 1, 1, 1),
        )
        self.total_driving_time_label.bind(size=self._update_text_size)
        total_driving_time_layout.add_widget(self.total_driving_time_label)

        total_driving_time_container.add_widget(total_driving_time_layout)

        middle_content.add_widget(total_driving_time_container)

        total_distance_driven_container = BoxLayout(
            orientation="vertical", spacing=5, size_hint=(1, 0.2)
        )  # change #1
        self.total_distance_driven_text_label = Label(  # 2
            text="Total Distance",
            font_size="40sp",
            halign="left",
            valign="middle",
            size_hint=(1, 0.2),
            color=(0, 1, 1, 1),
        )
        self.total_distance_driven_text_label.bind(
            size=self._update_text_size
        )  # change to #2
        total_distance_driven_container.add_widget(
            self.total_distance_driven_text_label
        )  # change to #1 and #2

        total_distance_driven_value_container = BoxLayout(
            orientation="horizontal", size_hint=(1, 0.2)
        )  # 3
        self.distance_driven = Label(  # change to #3, #4
            text="000",
            font_size="45sp",
            halign="left",
            valign="middle",
            size_hint_x=0.7,
            width=160,
            color=(1, 1, 1, 1),
        )
        self.distance_driven.bind(size=self._update_text_size)  # change to #4
        total_distance_driven_value_container.add_widget(self.distance_driven)
        total_distance_driven_container.add_widget(total_distance_driven_value_container)

        middle_content.add_widget(total_distance_driven_container)


        run_time_container = BoxLayout(
            orientation="vertical", spacing=5, size_hint=(1, 0.2)
        )  # change #1
        self.run_time_text_label = Label(  # 2
            text="Effscore",
            font_size="40sp",
            halign="left",
            valign="middle",
            size_hint=(1, 0.4),
            color=(0, 1, 1, 1),
        )
        self.run_time_text_label.bind(size=self._update_text_size)  # change to #2
        run_time_container.add_widget(self.run_time_text_label)  # change to #1 and #2

        run_time_value = BoxLayout(
            orientation="horizontal", size_hint=(1, 0.6), spacing=5
        )  # 3
        self.run_time_value_label = Label(  # change to #3, #4
            text="0",
            font_size="45sp",
            halign="left",
            valign="middle",
            size_hint_x=0.4,
            width=160,
            color=(1, 1, 1, 1),
        )
        self.run_time_value_label.bind(size=self._update_text_size)  # change to #4
        run_time_value.add_widget(self.run_time_value_label)
        run_time_container.add_widget(run_time_value)
        middle_content.add_widget(run_time_container)

        left_content = OutlinedBox(
            orientation="vertical", spacing=5, size_hint=(0.33, 1)
        )

        ## Middle section layout

        pack_max_temp_container = BoxLayout(
            orientation="vertical", spacing=5, size_hint=(1, 0.2)
        )  # change #1
        self.pack_max_temp_text_label = Label(  # 2
            text="Pack Temp Max",
            font_size="40sp",
            halign="left",
            valign="middle",
            size_hint=(1, 0.2),
            color=(0, 1, 1, 1),
        )
        self.pack_max_temp_text_label.bind(size=self._update_text_size)  # change to #2
        pack_max_temp_container.add_widget(
            self.pack_max_temp_text_label
        )  # change to #1 and #2

        pack_max_value = BoxLayout(orientation="horizontal", size_hint=(1, 0.2))  # 3
        self.pack_max_value_label = Label(  # change to #3, #4
            text="000",
            font_size="45sp",
            halign="left",
            valign="middle",
            size_hint_x=0.7,
            width=160,
            color=(1, 1, 1, 1),
        )
        self.pack_max_value_label.bind(size=self._update_text_size)  # change to #4
        pack_max_value.add_widget(self.pack_max_value_label)
        self.pack_max_temp_unit_label = Label(
            text="°C",
            font_size="45sp",
            halign="left",
            valign="middle",
            size_hint_x=2,
            width=60,
            color=(1, 1, 1, 1),
        )
        self.pack_max_temp_unit_label.bind(size=self._update_text_size)
        pack_max_value.add_widget(self.pack_max_temp_unit_label)
        pack_max_temp_container.add_widget(pack_max_value)
        left_content.add_widget(pack_max_temp_container)
        # här sneela

        pack_soc_used_container = BoxLayout(
            orientation="vertical", spacing=5, size_hint=(1, 0.2)
        )  # change #1
        self.pack_soc_used_text_label = Label(  # 2
            text="Pack SOC Used",
            font_size="40sp",
            halign="left",
            valign="middle",
            size_hint=(1, 0.4),
            color=(0, 1, 1, 1),
        )
        self.pack_soc_used_text_label.bind(size=self._update_text_size)  # change to #2
        pack_soc_used_container.add_widget(
            self.pack_soc_used_text_label
        )  # change to #1 and #2

        soc_used_layout = BoxLayout(
            orientation="horizontal", size_hint=(1, 0.6), spacing=5
        )  # 3
        self.soc_used_label = Label(  # change to #3, #4
            text="000",
            font_size="45sp",
            halign="left",
            valign="middle",
            size_hint_x=0.7,
            width=160,
            color=(1, 1, 1, 1),
        )
        self.soc_used_label.bind(size=self._update_text_size)  # change to #4
        soc_used_layout.add_widget(self.soc_used_label)
        pack_soc_used_container.add_widget(soc_used_layout)
        left_content.add_widget(pack_soc_used_container)

        pack_voltage_container = BoxLayout(
            orientation="vertical", spacing=5, size_hint=(1, 0.2)
        )
        self.pack_voltage_text_label = Label(
            text="Pack Voltage Min",
            font_size="40sp",
            halign="left",
            valign="middle",
            size_hint=(1, 0.4),
            color=(0, 1, 1, 1),
        )
        self.pack_voltage_text_label.bind(size=self._update_text_size)
        pack_voltage_container.add_widget(self.pack_voltage_text_label)

        voltage_value_layout = BoxLayout(
            orientation="horizontal", size_hint=(1, 0.6), spacing=5
        )
        self.voltage_value_label = Label(
            text="000",
            font_size="45sp",
            halign="left",
            valign="middle",
            size_hint_x=0.7,
            width=160,
            color=(1, 1, 1, 1),
        )
        self.voltage_value_label.bind(size=self._update_text_size)
        voltage_value_layout.add_widget(self.voltage_value_label)
        self.voltage_unit_label = Label(
            text="V",
            font_size="45sp",
            halign="left",
            valign="middle",
            size_hint_x=2,
            width=60,
            color=(1, 1, 1, 1),
        )
        self.voltage_unit_label.bind(size=self._update_text_size)
        voltage_value_layout.add_widget(self.voltage_unit_label)
        pack_voltage_container.add_widget(voltage_value_layout)
        left_content.add_widget(pack_voltage_container)

        # LV-bat temp-container

        orion_current_container = BoxLayout(
            orientation="vertical", size_hint=(1, 0.2)
        )  # 1/3 av vänster sida
        self.orion_current_text_label = Label(
            text="Orion Current Max",
            font_size="40sp",
            halign="left",
            valign="middle",
            size_hint=(1, 0.4),
            color=(0, 1, 1, 1),
        )
        self.orion_current_text_label.bind(size=self._update_text_size)
        orion_current_container.add_widget(self.orion_current_text_label)

        current_value_layout = BoxLayout(
            orientation="horizontal", size_hint=(1, 0.4), spacing=5
        )
        self.current_value_value_label = Label(
            text="000",
            font_size="45sp",
            halign="left",
            valign="middle",
            size_hint_x=0.7,
            width=160,  # Fast bredd så att värdet ser konsekvent ut
            color=(1, 1, 1, 1),
        )
        self.current_value_value_label.bind(size=self._update_text_size)
        current_value_layout.add_widget(self.current_value_value_label)
        self.current_unit_label = Label(
            text="A",
            font_size="45sp",
            halign="left",
            valign="middle",
            size_hint_x=2,
            width=60,  # Fast bredd för enhet
            color=(1, 1, 1, 1),
        )
        self.current_unit_label.bind(size=self._update_text_size)
        current_value_layout.add_widget(self.current_unit_label)
        orion_current_container.add_widget(current_value_layout)
        left_content.add_widget(orion_current_container)

        # Cell max temp-container
        watt_max_container = BoxLayout(
            orientation="vertical", spacing=5, size_hint=(1, 0.2)
        )
        self.watt_max_text_label = Label(
            text="Max Power",
            font_size="40sp",
            halign="left",
            valign="middle",
            size_hint=(1, 0.4),
            color=(0, 1, 1, 1),
        )
        self.watt_max_text_label.bind(size=self._update_text_size)
        watt_max_container.add_widget(self.watt_max_text_label)  # change to #1 and #2

        watt_value_value = BoxLayout(
            orientation="horizontal", size_hint=(1, 0.33), spacing=5
        )  # 3
        self.watt_value_value_label = Label(  # change to #3, #4
            text="000",
            font_size="45sp",
            halign="left",
            valign="middle",
            size_hint_x=0.7,
            width=160,
            color=(1, 1, 1, 1),
        )
        self.watt_value_value_label.bind(size=self._update_text_size)  # change to #4
        watt_value_value.add_widget(self.watt_value_value_label)
        self.watt_max_unit_label = Label(
            text="kW",
            font_size="45sp",
            halign="left",
            valign="middle",
            size_hint_x=2,
            width=60,
            color=(1, 1, 1, 1),
        )
        self.watt_max_unit_label.bind(size=self._update_text_size)
        watt_value_value.add_widget(self.watt_max_unit_label)
        watt_max_container.add_widget(watt_value_value)
        left_content.add_widget(watt_max_container)

        # Höger innehåll: Fel- och varningssektioner (placeras högerut)
        right_content = OutlinedBox(
            orientation="vertical", spacing=5, size_hint=(0.33, 1)
        )

        current_driving_time_state_container = BoxLayout(
            orientation="vertical", spacing=5, size_hint=(1, 0.2)
        )
        self.current_driving_time_state_text_label = Label(
            text="Current Driving Time",
            font_size="35sp",
            halign="left",
            valign="middle",
            size_hint=(1, 0.4),
            color=(0, 1, 1, 1),
        )
        self.current_driving_time_state_text_label.bind(size=self._update_text_size)
        current_driving_time_state_container.add_widget(
            self.current_driving_time_state_text_label
        )

        current_driving_time_state_layout = BoxLayout(
            orientation="horizontal", size_hint=(1, 0.6), spacing=5
        )
        self.current_driving_time_state_label = Label(
            text="N/A",
            font_size="45sp",
            halign="left",
            valign="middle",
            size_hint_x=0.3,
            width=160,
            color=(1, 1, 1, 1),
        )
        self.current_driving_time_state_label.bind(size=self._update_text_size)
        current_driving_time_state_layout.add_widget(
            self.current_driving_time_state_label
        )

        current_driving_time_state_container.add_widget(
            current_driving_time_state_layout
        )

        right_content.add_widget(current_driving_time_state_container)

        current_distance_container = BoxLayout(
            orientation="vertical", spacing=5, size_hint=(1, 0.2)
        )
        self.current_distance_text_label = Label(
            text="Current Distance Driven",
            font_size="35sp",
            halign="left",
            valign="middle",
            size_hint=(1, 0.4),
            color=(0, 1, 1, 1),
        )
        self.current_distance_text_label.bind(size=self._update_text_size)
        current_distance_container.add_widget(
            self.current_distance_text_label
        )  # change to #1 and #2

        energy_used_value_value = BoxLayout(
            orientation="horizontal", size_hint=(1, 0.33), spacing=5
        )  # 3
        self.energy_used_value_value_label = Label(  # change to #3, #4
            text="000",
            font_size="45sp",
            halign="left",
            valign="middle",
            size_hint_x=0.7,
            width=160,
            color=(1, 1, 1, 1),
        )
        self.energy_used_value_value_label.bind(
            size=self._update_text_size
        )  # change to #4
        energy_used_value_value.add_widget(self.energy_used_value_value_label)
        current_distance_container.add_widget(energy_used_value_value)
        right_content.add_widget(current_distance_container)

        energy_used_container = BoxLayout(
            orientation="vertical", spacing=5, size_hint=(1, 0.2)
        )
        self.energy_used_text_label = Label(
            text="Energy Used",
            font_size="40sp",
            halign="left",
            valign="middle",
            size_hint=(1, 0.4),
            color=(0, 1, 1, 1),
        )
        self.energy_used_text_label.bind(size=self._update_text_size)
        energy_used_container.add_widget(
            self.energy_used_text_label
        )  # change to #1 and #2

        energy_used_value = BoxLayout(
            orientation="horizontal", size_hint=(1, 0.33), spacing=5
        )  # 3
        self.energy_used_value_label = Label(  # change to #3, #4
            text="000",
            font_size="45sp",
            halign="left",
            valign="middle",
            size_hint_x=0.7,
            width=160,
            color=(1, 1, 1, 1),
        )
        self.energy_used_value_label.bind(size=self._update_text_size)  # change to #4
        energy_used_value.add_widget(self.energy_used_value_label)

        energy_used_container.add_widget(energy_used_value)
        right_content.add_widget(energy_used_container)

        content_layout.add_widget(left_content)
        content_layout.add_widget(middle_content)
        content_layout.add_widget(right_content)

        # Lägg ihop alla delar i huvudlayouten
        main_layout.add_widget(header_layout)
        main_layout.add_widget(separator)
        main_layout.add_widget(content_layout)

        self.add_widget(main_layout)

    def _update_text_size(self, instance, value):
        # Set text_size to the width only so the text does not wrap vertically
        instance.text_size = (instance.width, None)



    def refresh(self):

        self.orion_current_max = self.current_stats["orion_current_max"] # Fråga oliver hur fan dessa uppdateras?
        self.speed_max = self.current_stats["speed_max"]
        self.pack_temp_max = self.current_stats["pack_temp_max"]
        self.lv_bat_voltage_min = self.current_stats["lv_bat_voltage_min"]
        self.pack_voltage_min = self.current_stats["pack_voltage_min"]
        self.watt_max = self.current_stats["power_max"]
        self.total_run_time = self.presistant_stats["total_driving_time_s"]
        self.driving_time = self.current_stats["driving_time"]
        self.consumed_soc = self.current_stats["consumed_soc"]
        self.energy_drawn_kwh = self.current_stats["energy_drawn_wh"]
        self.distance_driven_m = self.current_stats["distance_driven_m"]
        self.total_distance_driven_m = self.presistant_stats["distance_driven_m"]
        self.effscore = self.current_stats["effscore"]

        # Updatera lables
        self.pack_max_value_label.text = f"{int(self.pack_temp_max)}"
        self.speed_max_value_label.text = f"{int(self.speed_max)}"
        self.lv_bat_low_value_label.text = f"{int(self.lv_bat_voltage_min)}"
        self.pack_soc_used_text_label = f"{int(self.consumed_soc)}"
        self.voltage_value_label.text = f"{int(self.pack_voltage_min)}"
        self.energy_used_value_label.text = self._format_energy(self.energy_drawn_kwh)
        self.current_value_value_label.text = f"{int(self.orion_current_max)}"
        self.energy_used_value_value_label.text = self._format_distance(self.distance_driven_m)
        self.distance_driven.text = self._format_distance(self.total_distance_driven_m)
        self.total_driving_time_label.text = self._format_time(self.total_run_time)
        self.current_driving_time_state_label.text = self._format_time(self.driving_time)
        self.run_time_value_label.text = f"{self.effscore:.3f}"
        self.watt_value_value_label.text = f"{int(self.watt_max)}"
        self.soc_used_label.text = f"{int(self.consumed_soc)} %"


    def _update_separator(self, instance, value):
        # Update the separator line's points based on the widget's current position and size
        self.separator_line.points = [
            instance.x,
            instance.y + instance.height / 2,
            instance.x + instance.width,
            instance.y + instance.height / 2,
        ]

    def _format_time(self, total_seconds):
        hours = int(total_seconds // 3600)
        minutes = int((total_seconds % 3600) // 60)
        seconds = int(total_seconds % 60)
        return f"{hours}h:{minutes:02}m:{seconds:01}s"

    def _format_distance(self, meters):
        if meters >= 1000:
            km = int(meters // 1000)
            m = int(meters % 1000)
            return f"{km} km : {m} m"
        else:
            return f"{int(meters)} m"

    def _format_energy(self, energy_wh):
        kwh = int(energy_wh // 1000)
        wh = int(energy_wh % 1000)
        return f"{kwh} kWh : {wh} Wh"

    #File resetter


    def reset_file(self, time):
        if time >= 3:
            print("Resetting stats...") # DEBUG KEY IS "O" hold for 3 sec
        # Reset the actual files
            self.stats_current.reset_file()
        # Reload the cleared data from disk
            self.current_stats = self.stats_current.load()
            self.shared_data.reset()


# Main App Class
class AfterdriveApp(App):
    def build(self):
        return Afterdrive()


if __name__ == "__main__":
    AfterdriveApp().run()
