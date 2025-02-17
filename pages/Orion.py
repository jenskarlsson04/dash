from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.graphics import Color, Line
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.image import Image
import os
import canparser
from can_reader import subscribe_can_message


class Orion(Screen):
    def __init__(self, **kwargs):
        super(Orion, self).__init__(**kwargs)
        # Variabler för data
        subscribe_can_message(canparser.OrionPowerData, self.update_pack_info)
        subscribe_can_message(canparser.OrionTempData, self.update_cell_temp)
        self.pack_current = 0
        self.pack_voltage = 0
        self.cell_temp_min = 0
        self.cell_temp_max = 0
        self.pack_soc = 0
        self.lv_bat_voltage = 12.3
        # Huvudlayout: Vertikal BoxLayout med header, separator och innehåll

        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # 1. HEADER (Debug - Logo - Orion)
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
        self.orion_label = Label(
            text='Orion',
            font_size='70sp',
            size_hint_x=0.3,
            color=(0, 1, 1, 1),
            halign='right',
            valign='middle'
        )
        header_layout.add_widget(self.debug_label)
        header_layout.add_widget(self.logo_image)
        header_layout.add_widget(self.orion_label)

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
        pack_current_container = BoxLayout(orientation='vertical', size_hint=(1, 0.33)) # 1/3 av vänster sida
        self.Pack_Current_text_label = Label(
            text='Pack Current',
            font_size='80sp',
            halign='left',
            valign='middle',
            size_hint=(1, 0.4),
            color=(0, 1, 1, 1)
        )
        self.Pack_Current_text_label.bind(size=self._update_text_size)
        pack_current_container.add_widget(self.Pack_Current_text_label)

        current_value_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.4), spacing=5)
        self.current_value_value_label = Label(
            text='000',
            font_size='120sp',
            halign='left',
            valign='middle',
            size_hint_x=0.3,
            width=160,  # Fast bredd så att värdet ser konsekvent ut
            color=(1, 1, 1, 1)
        )
        self.current_value_value_label.bind(size=self._update_text_size)
        current_value_layout.add_widget(self.current_value_value_label)
        self.current_unit_label = Label(
            text='A',
            font_size='120sp',
            halign='left',
            valign='middle',
            size_hint_x=0.5,
            width=60,  # Fast bredd för enhet
            color=(1, 1, 1, 1)
        )
        self.current_unit_label.bind(size=self._update_text_size)
        current_value_layout.add_widget(self.current_unit_label)
        pack_current_container.add_widget(current_value_layout)
        left_content.add_widget(pack_current_container)

        # Pack SOC-container
        pack_soc_container = BoxLayout(orientation='vertical', spacing=5, size_hint=(1, 0.33)) #change #1
        self.pack_soc_text_label = Label( #2
            text='Pack SOC',
            font_size='80sp',
            halign='left',
            valign='middle',
            size_hint=(1, 0.4),
            color=(0, 1, 1, 1)
        )
        self.pack_soc_text_label.bind(size=self._update_text_size) #change to #2
        pack_soc_container.add_widget(self.pack_soc_text_label) #change to #1 and #2

        soc_value_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.6), spacing=5) #3
        self.soc_value_label = Label( #change to #3, #4
            text='000',
            font_size='120sp',
            halign='left',
            valign='middle',
            size_hint_x=0.3,
            width=160,
            color=(1, 1, 1, 1)
        )
        self.soc_value_label.bind(size=self._update_text_size)  #change to #4
        soc_value_layout.add_widget(self.soc_value_label)
        self.soc_unit_label = Label(
            text='%',
            font_size='120sp',
            halign='left',
            valign='middle',
            size_hint_x=0.5,
            width=60,
            color=(1, 1, 1, 1)
        )
        self.soc_unit_label.bind(size=self._update_text_size)
        soc_value_layout.add_widget(self.soc_unit_label)
        pack_soc_container.add_widget(soc_value_layout)
        left_content.add_widget(pack_soc_container)

        # Motor Temperature-container
        pack_voltage_container = BoxLayout(orientation='vertical', spacing=5, size_hint=(1, 0.33))
        self.pack_voltage_text_label = Label(
            text='Pack Voltage',
            font_size='80sp',
            halign='left',
            valign='middle',
            size_hint=(1, 0.4),
            color=(0, 1, 1, 1)
        )
        self.pack_voltage_text_label.bind(size=self._update_text_size)
        pack_voltage_container.add_widget(self.pack_voltage_text_label)

        voltage_value_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.6), spacing=5)
        self.voltage_value_label = Label(
            text='000',
            font_size='120sp',
            halign='left',
            valign='middle',
            size_hint_x=0.3,
            width=160,
            color=(1, 1, 1, 1)
        )
        self.voltage_value_label.bind(size=self._update_text_size)
        voltage_value_layout.add_widget(self.voltage_value_label)
        self.voltage_unit_label = Label(
            text='V',
            font_size='120sp',
            halign='left',
            valign='middle',
            size_hint_x=0.5,
            width=60,
            color=(1, 1, 1, 1)
        )
        self.voltage_unit_label.bind(size=self._update_text_size)
        voltage_value_layout.add_widget(self.voltage_unit_label)
        pack_voltage_container.add_widget(voltage_value_layout)
        left_content.add_widget(pack_voltage_container)




        # Höger innehåll: Fel- och varningssektioner (placeras högerut)
        right_content = BoxLayout(orientation='vertical', spacing=10, size_hint=(0.5, 1))

        # Cell max temp-container
        cell_max_temp_container = BoxLayout(orientation='vertical', spacing=5, size_hint=(1, 0.5))  # change #1
        self.cell_max_temp_text_label = Label(  # 2
            text='Cell Max Temp',
            font_size='80sp',
            halign='right',
            valign='middle',
            size_hint=(1, 0.2),
            color=(0, 1, 1, 1)
        )
        self.cell_max_temp_text_label.bind(size=self._update_text_size)  # change to #2
        cell_max_temp_container.add_widget(self.cell_max_temp_text_label)  # change to #1 and #2

        cell_max_value = BoxLayout(orientation='horizontal', size_hint=(1, 0.33))  # 3
        self.cell_max_value_label = Label(  # change to #3, #4
            text='000',
            font_size='120sp',
            halign='right',
            valign='middle',
            size_hint_x=0.7,
            width=160,
            color=(1, 1, 1, 1)
        )
        self.cell_max_value_label.bind(size=self._update_text_size)  # change to #4
        cell_max_value.add_widget(self.cell_max_value_label)
        self.cell_max_temp_unit_label = Label(
            text='°C',
            font_size='120sp',
            halign='right',
            valign='middle',
            size_hint_x=0.2,
            width=60,
            color=(1, 1, 1, 1)
        )
        self.cell_max_temp_unit_label.bind(size=self._update_text_size)
        cell_max_value.add_widget(self.cell_max_temp_unit_label)
        cell_max_temp_container.add_widget(cell_max_value)
        right_content.add_widget(cell_max_temp_container)

        # Cell max temp-container
        cell_min_temp_container = BoxLayout(orientation='vertical', spacing=5, size_hint=(1, 0.5))  # change #1
        self.cell_min_temp_text_label = Label(  # 2
            text='Cell Min Temp',
            font_size='80sp',
            halign='right',
            valign='middle',
            size_hint=(1, 0.4),
            color=(0, 1, 1, 1)
        )
        self.cell_min_temp_text_label.bind(size=self._update_text_size)  # change to #2
        cell_min_temp_container.add_widget(self.cell_min_temp_text_label)  # change to #1 and #2

        cell_min_value = BoxLayout(orientation='horizontal', size_hint=(1, 0.33), spacing=5)  # 3
        self.cell_min_value_label = Label(  # change to #3, #4
            text='000',
            font_size='120sp',
            halign='right',
            valign='middle',
            size_hint_x=0.7,
            width=160,
            color=(1, 1, 1, 1)
        )
        self.cell_min_value_label.bind(size=self._update_text_size)  # change to #4
        cell_min_value.add_widget(self.cell_min_value_label)
        self.cell_min_temp_unit_label = Label(
            text='°C',
            font_size='120sp',
            halign='right',
            valign='middle',
            size_hint_x=0.2,
            width=60,
            color=(1, 1, 1, 1)
        )
        self.cell_min_temp_unit_label.bind(size=self._update_text_size)
        cell_min_value.add_widget(self.cell_min_temp_unit_label)
        cell_min_temp_container.add_widget(cell_min_value)
        right_content.add_widget(cell_min_temp_container)

        # LV-bat temp-container
        LV_bat_container = BoxLayout(orientation='vertical', spacing=5, size_hint=(1, 0.5))  # change #1
        self.lv_bat_voltage_text_label = Label(  # 2
            text='LV Bat Volt',
            font_size='80sp',
            halign='right',
            valign='middle',
            size_hint=(1, 0.4),
            color=(0, 1, 1, 1)
        )
        self.lv_bat_voltage_text_label.bind(size=self._update_text_size)  # change to #2
        LV_bat_container.add_widget(self.lv_bat_voltage_text_label)  # change to #1 and #2

        lv_bat_value = BoxLayout(orientation='horizontal', size_hint=(1, 0.33), spacing=5)  # 3
        self.lv_bat_value_label = Label(  # change to #3, #4
            text='000',
            font_size='120sp',
            halign='right',
            valign='middle',
            size_hint_x=0.7,
            width=160,
            color=(1, 1, 1, 1)
        )
        self.lv_bat_value_label.bind(size=self._update_text_size)  # change to #4
        lv_bat_value.add_widget(self.lv_bat_value_label)
        self.lv_bat_unit_label = Label(
            text='V',
            font_size='120sp',
            halign='right',
            valign='middle',
            size_hint_x=0.2,
            width=60,
            color=(1, 1, 1, 1)
        )
        self.lv_bat_unit_label.bind(size=self._update_text_size)
        lv_bat_value.add_widget(self.lv_bat_unit_label)
        LV_bat_container.add_widget(lv_bat_value)
        right_content.add_widget(LV_bat_container)



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
        self.current_value_value_label.text = f'{self.pack_current}'
        self.soc_value_label.text = f'{self.pack_soc}'
        self.voltage_value_label.text = f'{self.pack_voltage}'
        self.cell_min_value_label.text = f'{self.cell_temp_max}'
        self.cell_max_value_label.text= f'{self.cell_temp_min}'
        self.lv_bat_value_label.text = f'{self.lv_bat_voltage}'


    # CAN-meddelandeuppdaterare
    #def update_pack_current(self, message):
    #    self.pack_current = round(message.parsed_data.

    # CAN-meddelandeuppdaterare
    def update_pack_info(self, message):
        self.pack_soc = round(100*(message.parsed_data.pack_soc_ratio))
        self.pack_current = round(message.parsed_data.pack_current_A)
        self.pack_voltage = round(message.parsed_data.pack_voltage_v)

    def update_cell_temp(self, message):
        self.cell_temp_max = round(message.parsed_data.pack_max_cell_temp_c)
        self.cell_temp_min = round(message.parsed_data.pack_min_cell_temp_c)

    def _update_separator(self, instance, value):
        # Update the separator line's points based on the widget's current position and size
        self.separator_line.points = [instance.x, instance.y + instance.height / 2,
                                        instance.x + instance.width, instance.y + instance.height / 2]


class OrionApp(App):
    def build(self):
        return Orion()


if __name__ == '__main__':
    Orion().run()
