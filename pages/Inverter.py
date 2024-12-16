from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import Screen
from kivy.graphics import Color, Line
from kivy.core.window import Window
import os
from kivy.uix.image import Image
from kivy.uix.scrollview import ScrollView
import canparser
from can_reader import subscribe_can_message


class Inverter(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Variabler för data
        self.inverter_temp = 0
        self.motortemp = 0
        subscribe_can_message(canparser.MotorTemperatureData, self.update_motor_temp)
        subscribe_can_message(canparser.InverterErrorsData, self.update_inverter_error)
        subscribe_can_message(canparser.InverterTemperatureData, self.update_inverter_temp)
        self.errors = []
        self.warnings = []

        # Huvudlayout
        main_layout = FloatLayout()

        # Huvudetikett
        self.inverter_label = Label(
            text='Inverter', font_size='70sp', size_hint=(0.2, 0.1),
            pos_hint={'x': 0, 'y': 0.88}, color=(0, 1, 1, 1)
        )

        self.debug_label = Label(
            text='Debug', font_size='70sp', size_hint=(0.2, 0.1),
            pos_hint={'x': 0.81, 'y': 0.88}, color=(0, 1, 1, 1)
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
            text='Inverter Temp', font_size='80sp', size_hint=(0.36, 0.2),
            pos_hint={'x': 0, 'y': 0.59}, color=(0, 1, 1, 1)
        )
        self.inverter_temp_value_label = Label(
            text='000', font_size='120sp', size_hint=(0.15, 0.1),
            pos_hint={'x': 0.03, 'y': 0.49}, color=(1, 1, 1, 1)
        )
        self.inverter_unit_label = Label(
            text='°C', font_size='120sp', size_hint=(0.1, 0.1),
            pos_hint={'x': 0.19, 'y': 0.49}, color=(1, 1, 1, 1)
        )

        # Motortemperatur
        self.motortemp_label = Label(
            text='Motor Temp', font_size='80sp', size_hint=(0.32, 0.2),
            pos_hint={'x': 0, 'y': 0.29}, color=(0, 1, 1, 1)
        )
        self.motortemp_value_label = Label(
            text='000', font_size='120sp', size_hint=(0.15, 0.1),
            pos_hint={'x': 0.03, 'y': 0.19}, color=(1, 1, 1, 1)
        )
        self.motortemp_unit_label = Label(
            text='°C', font_size='120sp', size_hint=(0.1, 0.1),
            pos_hint={'x': 0.19, 'y': 0.19}, color=(1, 1, 1, 1)
        )

        # ScrollView för fel
        self.errors_label = Label(
            text='Inverter Errors', font_size='50sp', size_hint=(0.2, 0.1),
            pos_hint={'x': 0.561, 'y': 0.63}, color=(0, 1, 1, 1)
        )
        self.errors_amount_label = Label(
            text='(0)', font_size='50sp', size_hint=(0.1, 0.1),
            pos_hint={'x': 0.82, 'y': 0.63}, color=(0, 1, 1, 1)
        )
        self.scroll_view_errors = ScrollView(
            size_hint=(1.5, 0.4),
            pos_hint={'x': -0.561, 'y': 0.24},
            do_scroll_x=False,
            do_scroll_y=True
        )
        self.errors_content_layout = FloatLayout(size_hint_y=0.7)
        self.scroll_view_errors.add_widget(self.errors_content_layout)

        # ScrollView för varningar
        self.warn_label = Label(
            text='Inverter Warnings', font_size='50sp', size_hint=(0.2, 0.1),
            pos_hint={'x': 0.585, 'y': 0.33}, color=(0, 1, 1, 1)
        )
        self.warn_amount_label = Label(
            text='(0)', font_size='50sp', size_hint=(0.1, 0.1),
            pos_hint={'x': 0.82, 'y': 0.33}, color=(0, 1, 1, 1)
        )
        self.scroll_view_warn = ScrollView(
            size_hint=(1.5, 0.4),
            pos_hint={'x': -0.561, 'y': -0.05},
            do_scroll_x=False,
            do_scroll_y=True
        )
        self.warn_content_layout = FloatLayout(size_hint_y=0.7)
        self.scroll_view_warn.add_widget(self.warn_content_layout)



        # Linje högst upp

        with main_layout.canvas:
            Color(1, 1, 2, 0.5)  # grey line
            # Line placed dynamically based on screen height and width
            Line(points=[0, Window.height * 1.20, Window.width * 1.5, Window.height * 1.20], width=8)




        # Lägg till widgets till huvudlayouten
        main_layout.add_widget(self.inverter_label)
        main_layout.add_widget(self.debug_label)
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
        # self.motortemp = random.randint(0, 120)
        self.inverter_temp_value_label.text = f'{self.inverter_temp}'
        self.motortemp_value_label.text = f'{self.motortemp}'


        # Error handling
        error_count = len(self.errors)
        self.errors_amount_label.text = f'({error_count})'
        self.errors_content_layout.clear_widgets()  # Clear old widgets
        display_errors = self.errors[:2]
        item_height = 50  # Height of each error label
        item_margin = 110  # Margin/spacing between each label
        self.errors_content_layout.height = max(len(display_errors) * (item_height + item_margin), self.scroll_view_errors.height)

        for i, error in enumerate(display_errors):
            label = Label(
                text=error,
                font_size='42sp',
                size_hint=(0.2, 0.6),
                size=(400, item_height),
                text_size=(400, 450),  # Set the text wrapping width
                halign='left',  # Horizontal alignment
                valign='middle',  # Vertical alignment
                pos_hint={
                    'x': 0.743,
                    'y': 1 - ((i + 1) * (item_height + item_margin) / self.errors_content_layout.height)
                },
                color=(1, 0, 0, 1)  # Red text for errors
            )
            label.bind(size=lambda instance, size: setattr(instance, 'text_size', size))  # Wrap text dynamically
            self.errors_content_layout.add_widget(label)

        # Warning handling
        warn_count = len(self.warnings)
        display_warn = self.warnings[:2]
        self.warn_amount_label.text = f'({warn_count})'
        self.warn_content_layout.clear_widgets()  # Clear old widgets
        self.warn_content_layout.height = max(len(display_warn) * (item_height + item_margin), self.scroll_view_warn.height)

        for i, warn in enumerate(display_warn):
            label = Label(
                text=warn,
                font_size='42sp',
                size_hint=(0.33, 0.54),
                size=(500, item_height),
                text_size=(400, 450),  # Set the text wrapping width
                halign='left',  # Horizontal alignment
                valign='middle',  # Vertical alignment
                pos_hint={
                    'x': 0.743,
                    'y': 1 - ((i + 1) * (item_height + item_margin) / self.warn_content_layout.height)
                },
                color=(1, 0, 0, 1)  # Red text for errors
            )
            label.bind(size=lambda instance, size: setattr(instance, 'text_size', size))  # Wrap text dynamically
            self.warn_content_layout.add_widget(label)


    # simulating different errors
    def update_motor_temp(self, message):
        self.motortemp = round(message.parsed_data.temperature_c)

    def update_inverter_temp(self, message):
        self.inverter_temp = round(message.parsed_data.temperature_c)

    def update_inverter_error(self, message):
        if message.parsed_data.decoded_errors:
            self.errors = [error.type for error in message.parsed_data.decoded_errors]
        if message.parsed_data.decoded_warnings:
            self.warnings = [warning.type for warning in message.parsed_data.decoded_warnings]

# Main App Class
class InverterDebug(App):
    def build(self):
        return Inverter()


if __name__ == '__main__':
    InverterDebug().run()
