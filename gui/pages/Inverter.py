from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.graphics import Color, Line
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.uix.scrollview import ScrollView
import os
import canparser
from can_reader import subscribe_can_message


class Inverter(Screen):
    def __init__(self, **kwargs):
        super(Inverter, self).__init__(**kwargs)
        # Variabler för data
        self.inverter_temp = 0
        self.motortemp = 0
        subscribe_can_message(canparser.MotorTemperatureData, self.update_motor_temp)
        subscribe_can_message(canparser.InverterErrorsData, self.update_inverter_error)
        subscribe_can_message(canparser.InverterTemperatureData, self.update_inverter_temp)
        self.errors = []
        self.warnings = []

        # Huvudlayout: Vertikal BoxLayout med header, separator och innehåll
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # 1. HEADER (Debug - Logo - Inverter)
        header_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.15))
        self.debug_label = Label(
            text='Debug',
            font_size='70sp',
            size_hint_x=0.3,
            color=(0, 1, 1, 1),
            halign='left',
            valign='middle'
        )
        image_path = os.path.join('./images/logo.png')
        self.logo_image = Image(
            source=image_path,
            opacity=0.15,
            allow_stretch=True,
            keep_ratio=True,
            size_hint_x=0.4
        )
        self.inverter_label = Label(
            text='Inverter',
            font_size='70sp',
            size_hint_x=0.3,
            color=(0, 1, 1, 1),
            halign='right',
            valign='middle'
        )
        header_layout.add_widget(self.debug_label)
        header_layout.add_widget(self.logo_image)
        header_layout.add_widget(self.inverter_label)

        # 2. SEPARATOR (Linje direkt under headern) - integrated here
        separator = Widget(size_hint=(1, None), height=5)
        with separator.canvas:
            Color(1, 1, 2, 0.5)
            self.separator_line = Line(points=[], width=8)
        separator.bind(pos=self._update_separator, size=self._update_separator)

        # 3. CONTENT (Temperatur- samt fel-/varningssektioner)
        content_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint=(1, 0.85))

        # Vänster innehåll: Temperaturavsnitt
        left_content = BoxLayout(orientation='vertical', spacing=10, size_hint=(0.5, 1))

        # Inverter Temperature-container
        inverter_temp_container = BoxLayout(orientation='vertical', size_hint=(1, 0.5))
        self.inverter_temp_text_label = Label(
            text='Inverter Temp',
            font_size='80sp',
            halign='left',
            valign='middle',
            size_hint=(1, 0.4),
            color=(0, 1, 1, 1)
        )
        self.inverter_temp_text_label.bind(size=self._update_text_size)
        inverter_temp_container.add_widget(self.inverter_temp_text_label)

        inverter_value_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.4), spacing=5)
        self.inverter_temp_value_label = Label(
            text='000',
            font_size='120sp',
            halign='left',
            valign='middle',
            size_hint_x=0.3,
            width=160,  # Fast bredd så att värdet ser konsekvent ut
            color=(1, 1, 1, 1)
        )
        self.inverter_temp_value_label.bind(size=self._update_text_size)
        inverter_value_layout.add_widget(self.inverter_temp_value_label)
        self.inverter_unit_label = Label(
            text='°C',
            font_size='120sp',
            halign='left',
            valign='middle',
            size_hint_x=0.5,
            width=60,  # Fast bredd för enhet
            color=(1, 1, 1, 1)
        )
        self.inverter_unit_label.bind(size=self._update_text_size)
        inverter_value_layout.add_widget(self.inverter_unit_label)
        inverter_temp_container.add_widget(inverter_value_layout)
        left_content.add_widget(inverter_temp_container)

        # Motor Temperature-container
        motor_temp_container = BoxLayout(orientation='vertical', spacing=5, size_hint=(1, 0.5))
        self.motortemp_text_label = Label(
            text='Motor Temp',
            font_size='80sp',
            halign='left',
            valign='middle',
            size_hint=(1, 0.4),
            color=(0, 1, 1, 1)
        )
        self.motortemp_text_label.bind(size=self._update_text_size)
        motor_temp_container.add_widget(self.motortemp_text_label)

        motor_value_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.6), spacing=5)
        self.motortemp_value_label = Label(
            text='000',
            font_size='120sp',
            halign='left',
            valign='middle',
            size_hint_x=0.3,
            width=160,
            color=(1, 1, 1, 1)
        )
        self.motortemp_value_label.bind(size=self._update_text_size)
        motor_value_layout.add_widget(self.motortemp_value_label)
        self.motortemp_unit_label = Label(
            text='°C',
            font_size='120sp',
            halign='left',
            valign='middle',
            size_hint_x=0.5,
            width=60,
            color=(1, 1, 1, 1)
        )
        self.motortemp_unit_label.bind(size=self._update_text_size)
        motor_value_layout.add_widget(self.motortemp_unit_label)
        motor_temp_container.add_widget(motor_value_layout)
        left_content.add_widget(motor_temp_container)

        # Höger innehåll: Fel- och varningssektioner (placeras högerut)
        right_content = BoxLayout(orientation='vertical', spacing=10, size_hint=(0.5, 1))

        # Fel-sektion
        error_section = BoxLayout(orientation='vertical', spacing=20, size_hint=(1, 0.4))
        error_title_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.4), spacing=5)
        self.errors_label = Label(
            text='Inverter Errors',
            font_size='50sp',
            halign='right',
            valign='middle',
            size_hint=(1, 1),
            color=(0, 1, 1, 1)
        )
        error_title_layout.add_widget(self.errors_label)
        self.errors_amount_label = Label(
            text='(0)',
            font_size='50sp',
            halign='right',
            valign='middle',
            size_hint=(0.1, 1),
            color=(0, 1, 1, 1)
        )
        error_title_layout.add_widget(self.errors_amount_label)
        error_section.add_widget(error_title_layout)

        self.scroll_view_errors = ScrollView(size_hint=(1, 0.8), do_scroll_x=False, do_scroll_y=True)
        self.errors_content_layout = BoxLayout(orientation='vertical', spacing=10, size_hint_y=None)
        self.errors_content_layout.bind(minimum_height=self.errors_content_layout.setter('height'))
        self.scroll_view_errors.add_widget(self.errors_content_layout)
        error_section.add_widget(self.scroll_view_errors)
        right_content.add_widget(error_section)

        # Varnings-sektion
        warn_section = BoxLayout(orientation='vertical', spacing=20, size_hint=(1, 0.4))
        warn_title_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.2))
        self.warn_label = Label(
            text='Inverter Warnings',
            font_size='50sp',
            halign='right',
            valign='middle',
            size_hint=(1, 1),
            color=(0, 1, 1, 1)
        )
        warn_title_layout.add_widget(self.warn_label)
        self.warn_amount_label = Label(
            text='(0)',
            font_size='50sp',
            halign='right',
            valign='middle',
            size_hint=(0.1, 1),
            color=(0, 1, 1, 1)
        )
        warn_title_layout.add_widget(self.warn_amount_label)
        warn_section.add_widget(warn_title_layout)

        self.scroll_view_warn = ScrollView(size_hint=(1, 0.8), do_scroll_x=False, do_scroll_y=True)
        self.warn_content_layout = BoxLayout(orientation='vertical', spacing=10, size_hint_y=None)
        self.warn_content_layout.bind(minimum_height=self.warn_content_layout.setter('height'))
        self.scroll_view_warn.add_widget(self.warn_content_layout)
        warn_section.add_widget(self.scroll_view_warn)
        right_content.add_widget(warn_section)

        content_layout.add_widget(left_content)
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
        # Uppdatera temperaturer
        self.inverter_temp_value_label.text = f'{self.inverter_temp}'
        self.motortemp_value_label.text = f'{self.motortemp}'

        # Uppdatera fel
        error_count = len(self.errors)
        self.errors_amount_label.text = f'({error_count})'
        self.errors_content_layout.clear_widgets()
        errors_to_show = self.errors[:2]
        for i, error in enumerate(errors_to_show):
            label = Label(
                text=error,
                font_size='55sp',
                size_hint_y=None,
                height=80,  # increased height for better spacing
                halign='right',
                valign='middle',
                color=(1, 0, 0, 1)
            )
            label.bind(size=self._update_text_size)
            self.errors_content_layout.add_widget(label)
            if i < len(errors_to_show) - 1:
                spacer = Widget(size_hint_y=None, height=30)
                self.errors_content_layout.add_widget(spacer)

        # Uppdatera varningar
        warn_count = len(self.warnings)
        self.warn_amount_label.text = f'({warn_count})'
        self.warn_content_layout.clear_widgets()
        warnings_to_show = self.warnings[:2]
        for i, warn in enumerate(warnings_to_show):
            label = Label(
                text=warn,
                font_size='44sp',
                size_hint_y=None,
                height=75,  # increased height
                halign='right',
                valign='middle',
                color=(1, 0, 0, 1)
            )
            label.bind(size=self._update_text_size)
            self.warn_content_layout.add_widget(label)
            if i < len(warnings_to_show) - 1:
                spacer = Widget(size_hint_y=None, height=30)
                self.warn_content_layout.add_widget(spacer)

    # CAN-meddelandeuppdaterare
    def update_motor_temp(self, message):
        self.motortemp = round(message.parsed_data.temperature_c)

    def update_inverter_temp(self, message):
        self.inverter_temp = round(message.parsed_data.temperature_c)

    def update_inverter_error(self, message):
        if message.parsed_data.decoded_errors:
            self.errors = [error.type for error in message.parsed_data.decoded_errors]
        if message.parsed_data.decoded_warnings:
            self.warnings = [warning.type for warning in message.parsed_data.decoded_warnings]

    def _update_separator(self, instance, value):
        # Update the separator line's points based on the widget's current position and size
        self.separator_line.points = [instance.x, instance.y + instance.height / 2,
                                        instance.x + instance.width, instance.y + instance.height / 2]


class InverterDebug(App):
    def build(self):
        return Inverter()


if __name__ == '__main__':
    InverterDebug().run()
