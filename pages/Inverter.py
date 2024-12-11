import random
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import Screen
import os
from kivy.uix.image import Image
from kivy.uix.scrollview import ScrollView
import canparser
from can_reader import subscribe_can_message


class Inverter(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)



        # Variabler för data
        self.inverter_temp = 100
        self.motortemp = 100
        subscribe_can_message(canparser.InverterTemperatureData, self.inverter_temp)

        self.errors = [
            "Parameter conflict detected",
            "Special CPU Fault",
            "RFE input not present",
            "Auxiliary Voltage Min. Limit",
            "Feedback Signal problem",
            "Warn. 5",
            "Motor-Temperature (>87%)",
            "IGBT Temperature (>87%)",
           "Vout Saturation Max. Limit",
            "Warn. 9",
            "SpeedActual resolution Limit",
            "Check ECode ID: 0x94",
            "Tripzone Glitch detected",
            "ADC Sequencer problem",
            "ADC Measurement problem",
            "Bleeder resistor load (>87%)",
        ]
        self.warn = [
            "Eprom Read Error",
        "HW Fault",
        "RFE input not present",
        "CAN TimeOut Error",
        "Feedback Signal Error",
        "Mains Voltage Min. Limit",
        "Motor-Temp. Max. Limit",
        "IGBT-Temp. Max. Limit",
        "Mains Voltage Max. Limit",
        "Critical AC Current",
        "Race Away detected",
        "ECode TimeOut Error",
        "Watchdog Reset",
        "I Offset problem",
        "Internal HW voltage problem",
        "Bleed resistor overload"
        ]

        # Huvudlayout
        main_layout = FloatLayout()

        # Huvudetikett
        self.inverter_label = Label(
            text='Inverter', font_size='70sp', size_hint=(0.1, 0.1),
            pos_hint={'x': 0.05, 'y': 0.85}, color=(0, 1, 1, 1)
        )

        # Logotyp med låg opacitet
        image_path = os.path.join('./images/logo.png')
        self.logo_image = Image(
            source=image_path,
            opacity=0.15,
            allow_stretch=True,
            keep_ratio=True,
            size_hint=(0.15, 0.15),
            pos_hint={'center_x': 0.5, 'center_y': 0.93}
        )

        # Invertertemperatur
        self.inverter_temp_label = Label(
            text='Inverter Temp', font_size='80sp', size_hint=(None, None),
            pos_hint={'x': 0.14, 'y': 0.69}, color=(0, 1, 1, 1)
        )
        self.inverter_temp_value_label = Label(
            text='000', font_size='80sp', size_hint=(None, None),
            pos_hint={'x': 0.02, 'y': 0.54}, color=(1, 1, 1, 1)
        )
        self.inverter_unit_label = Label(
            text='C', font_size='80sp', size_hint=(None, None),
            pos_hint={'x': 0.10, 'y': 0.54}, color=(1, 1, 1, 1)
        )

        # Motortemperatur
        self.motortemp_label = Label(
            text='Motor Temp', font_size='80sp', size_hint=(None, None),
            pos_hint={'x': 0.12, 'y': 0.39}, color=(0, 1, 1, 1)
        )
        self.motortemp_value_label = Label(
            text='000', font_size='80sp', size_hint=(None, None),
            pos_hint={'x': 0.02, 'y': 0.23}, color=(1, 1, 1, 1)
        )
        self.motortemp_unit_label = Label(
            text='C', font_size='80sp', size_hint=(None, None),
            pos_hint={'x': 0.10, 'y': 0.23}, color=(1, 1, 1, 1)
        )

        # ScrollView för fel
        self.errors_label = Label(
            text='Inverter Errors', font_size='50sp', size_hint=(None, None),
            pos_hint={'x': 0.687, 'y': 0.87}, color=(0, 1, 1, 1)
        )
        self.errors_amount_label = Label(
            text='(0)', font_size='50sp', size_hint=(None, None),
            pos_hint={'x': 0.91, 'y': 0.87}, color=(0, 1, 1, 1)
        )
        self.scroll_view_errors = ScrollView(
            size_hint=(1.2, 0.4),
            pos_hint={'x': -0.28, 'y': 0.5},
            do_scroll_x=False,
            do_scroll_y=True
        )
        self.errors_content_layout = FloatLayout(size_hint_y=None)
        self.scroll_view_errors.add_widget(self.errors_content_layout)

        # ScrollView för varningar
        self.warn_label = Label(
            text='Inverter Warnings', font_size='50sp', size_hint=(None, None),
            pos_hint={'x': 0.713, 'y': 0.47}, color=(0, 1, 1, 1)
        )
        self.warn_amount_label = Label(
            text='(0)', font_size='50sp', size_hint=(None, None),
            pos_hint={'x': 0.91, 'y': 0.47}, color=(0, 1, 1, 1)
        )
        self.scroll_view_warn = ScrollView(
            size_hint=(1.2, 0.4),
            pos_hint={'x': -0.28, 'y': 0.05},
            do_scroll_x=False,
            do_scroll_y=True
        )
        self.warn_content_layout = FloatLayout(size_hint_y=None)
        self.scroll_view_warn.add_widget(self.warn_content_layout)

        # Lägg till widgets till huvudlayouten
        main_layout.add_widget(self.inverter_label)
        main_layout.add_widget(self.logo_image)
        main_layout.add_widget(self.inverter_temp_label)
        main_layout.add_widget(self.inverter_temp_value_label)
        main_layout.add_widget(self.inverter_unit_label)
        main_layout.add_widget(self.motortemp_label)
        main_layout.add_widget(self.motortemp_value_label)
        main_layout.add_widget(self.motortemp_unit_label)
        main_layout.add_widget(self.errors_label)
        main_layout.add_widget(self.errors_amount_label)
        main_layout.add_widget(self.scroll_view_errors)
        main_layout.add_widget(self.warn_label)
        main_layout.add_widget(self.warn_amount_label)
        main_layout.add_widget(self.scroll_view_warn)

        # Lägg till layouten till skärmen
        self.add_widget(main_layout)


    def refresh(self):
        # Randomize temperatures
        #self.inverter_temp = random.randint(0, 120)
        self.motortemp = random.randint(0, 120)
        self.inverter_temp_value_label.text = f'{self.inverter_temp}'
        self.motortemp_value_label.text = f'{self.motortemp}'

        # Inverter CAN sub
    def update_inverter_temp(self, message):
        self.inverter_temp = round(message.parsed_data.inverter_temp)

        # Error handling
        error_count = len(self.errors)
        self.errors_amount_label.text = f'({error_count})'
        self.errors_content_layout.clear_widgets()  # Clear old widgets
        display_errors = random.sample(self.errors, min(2, error_count))
        item_height = 100  # Height of each error label
        item_margin = 40  # Margin/spacing between each label
        self.errors_content_layout.height = len(display_errors) * (item_height + item_margin)



        for i, error in enumerate(display_errors):
            label = Label(
                text=error,
                font_size='50sp',
                size_hint=(None, None),
                size=(400, item_height),
                text_size=(450, 500),  # Set the text wrapping width
                halign='left',  # Horizontal alignment
                valign='middle',  # Vertical alignment
                pos_hint={
                    'x': 0.76,
                    'y': 1 - ((i + 1) * (item_height + item_margin) / self.errors_content_layout.height)
                },
                color=(1, 0, 0, 1)  # Red text for errors
            )
            label.bind(size=lambda instance, size: setattr(instance, 'text_size', size))  # Wrap text dynamically
            self.errors_content_layout.add_widget(label)

        # Warning handling
        warn_count = len(self.warn)
        self.warn_amount_label.text = f'({warn_count})'
        self.warn_content_layout.clear_widgets()  # Clear old widgets
        display_warn = random.sample(self.warn, min(2, error_count))
        self.warn_content_layout.height = len(display_warn) * (item_height + item_margin)

        for i, warn in enumerate(display_warn):
            label = Label(
                text=warn,
                font_size='50sp',
                size_hint=(None, None),
                size=(400, item_height),
                text_size=(450, 500),  # Set the text wrapping width
                halign='left',  # Horizontal alignment
                valign='middle',  # Vertical alignment
                pos_hint={
                    'x': 0.76,
                    'y': 1 - ((i + 1) * (item_height + item_margin) / self.warn_content_layout.height)
                },
                color=(1, 0, 0, 1)  # Red text for errors
            )
            label.bind(size=lambda instance, size: setattr(instance, 'text_size', size))  # Wrap text dynamically
            self.warn_content_layout.add_widget(label)
    # simulating different errors



# Main App Class
class InverterDebug(App):
    def build(self):
        return Inverter()


if __name__ == '__main__':
    InverterDebug().run()
