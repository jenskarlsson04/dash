from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.graphics import Color, Line
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.image import Image
import os
from gui.widgets.OutlinedBox import OutlinedBox
from shared_data import SharedDataDriver


class TSAC(Screen):
    def __init__(self, **kwargs):
        super(TSAC, self).__init__(**kwargs)
        self.SharedData = SharedDataDriver()

        # Huvudlayout: Vertikal BoxLayout med header, separator och innehåll

        main_layout = BoxLayout(orientation="vertical", padding=10, spacing=10)

        # 1. HEADER (Debug - Logo - Orion)
        header_layout = BoxLayout(orientation="horizontal", size_hint=(1, 0.15))
        self.debug_label = Label(
            text="Debug",
            font_size="70sp",
            size_hint_x=0.3,
            color=(0, 1, 1, 1),
            halign="left",
            valign="middle",
        )
        image_path = os.path.join("./gui/images/logo.png")
        self.logo_image = Image(
            source=image_path,
            opacity=0.15,
            allow_stretch=True,
            keep_ratio=True,
            size_hint_x=0.4,
        )
        self.tscu_label = Label(
            text="TSAC",
            font_size="70sp",
            size_hint_x=0.3,
            color=(0, 1, 1, 1),
            halign="right",
            valign="middle",
        )
        header_layout.add_widget(self.debug_label)
        header_layout.add_widget(self.logo_image)
        header_layout.add_widget(self.tscu_label)

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

        # Inverter Temperature-container
        tscu_state_container = BoxLayout(
            orientation="vertical", size_hint=(1, 0.2)
        )  # 1/3 av vänster sida
        self.TSCU_STATE_text_label = Label(
            text="TSCU STATE",
            font_size="40sp",
            halign="left",
            valign="middle",
            size_hint=(1, 0.4),
            color=(0, 1, 1, 1),
        )
        self.TSCU_STATE_text_label.bind(size=self._update_text_size)
        tscu_state_container.add_widget(self.TSCU_STATE_text_label)

        tscu_state_layout = BoxLayout(
            orientation="horizontal", size_hint=(1, 0.4), spacing=5
        )
        self.tscu_state_label = Label(
            text="N/A",
            font_size="35sp",
            halign="left",
            valign="middle",
            size_hint_x=0.3,
            width=170,  # Fast bredd så att värdet ser konsekvent ut
            color=(1, 1, 1, 1),
        )
        self.tscu_state_label.bind(size=self._update_text_size)
        tscu_state_layout.add_widget(self.tscu_state_label)
        tscu_state_container.add_widget(tscu_state_layout)
        middle_content.add_widget(tscu_state_container)

        # Pack SOC-container
        tscu_mode_container = BoxLayout(
            orientation="vertical", spacing=5, size_hint=(1, 0.2)
        )  # change #1
        self.tscu_mode_text_label = Label(  # 2
            text="TSCU MODE",
            font_size="40sp",
            halign="left",
            valign="middle",
            size_hint=(1, 0.4),
            color=(0, 1, 1, 1),
        )
        self.tscu_mode_text_label.bind(size=self._update_text_size)  # change to #2
        tscu_mode_container.add_widget(self.tscu_mode_text_label)  # change to #1 and #2

        tscu_mode_layout = BoxLayout(
            orientation="horizontal", size_hint=(1, 0.6), spacing=5
        )  # 3
        self.tscu_mode_label = Label(  # change to #3, #4
            text="N/A",
            font_size="45sp",
            halign="left",
            valign="middle",
            size_hint_x=0.3,
            width=160,
            color=(1, 1, 1, 1),
        )
        self.tscu_mode_label.bind(size=self._update_text_size)  # change to #4
        tscu_mode_layout.add_widget(self.tscu_mode_label)

        tscu_mode_container.add_widget(tscu_mode_layout)
        middle_content.add_widget(tscu_mode_container)

        # Motor Temperature-container
        airplus_state_container = BoxLayout(
            orientation="vertical", spacing=5, size_hint=(1, 0.2)
        )
        self.airplus_state_text_label = Label(
            text="AIR+",
            font_size="40sp",
            halign="left",
            valign="middle",
            size_hint=(1, 0.4),
            color=(0, 1, 1, 1),
        )
        self.airplus_state_text_label.bind(size=self._update_text_size)
        airplus_state_container.add_widget(self.airplus_state_text_label)

        airplus_state_layout = BoxLayout(
            orientation="horizontal", size_hint=(1, 0.6), spacing=5
        )
        self.airplus_state_label = Label(
            text="N/A",
            font_size="45sp",
            halign="left",
            valign="middle",
            size_hint_x=0.2,
            width=160,
            color=(1, 1, 1, 1),
        )
        self.airplus_state_label.bind(size=self._update_text_size)
        airplus_state_layout.add_widget(self.airplus_state_label)

        airplus_state_container.add_widget(airplus_state_layout)
        middle_content.add_widget(airplus_state_container)
        # Motor Temperature-container
        airminus_state_container = BoxLayout(
            orientation="vertical", spacing=5, size_hint=(1, 0.2)
        )
        self.airminus_state_text_label = Label(
            text="AIR-",
            font_size="40sp",
            halign="left",
            valign="middle",
            size_hint=(1, 0.4),
            color=(0, 1, 1, 1),
        )
        self.airminus_state_text_label.bind(size=self._update_text_size)
        airminus_state_container.add_widget(self.airminus_state_text_label)

        airminus_state_layout = BoxLayout(
            orientation="horizontal", size_hint=(1, 0.6), spacing=5
        )
        self.airminus_state_label = Label(
            text="N/A",
            font_size="45sp",
            halign="left",
            valign="middle",
            size_hint_x=0.3,
            width=160,
            color=(1, 1, 1, 1),
        )
        self.airminus_state_label.bind(size=self._update_text_size)
        airminus_state_layout.add_widget(self.airminus_state_label)

        airminus_state_container.add_widget(airminus_state_layout)

        middle_content.add_widget(airminus_state_container)

        SDC_status_container = BoxLayout(
            orientation="vertical", spacing=5, size_hint=(1, 0.2)
        )  # change #1
        self.SDC_status_text_label = Label(  # 2
            text="TSCU SDC",
            font_size="40sp",
            halign="left",
            valign="middle",
            size_hint=(1, 0.4),
            color=(0, 1, 1, 1),
        )
        self.SDC_status_text_label.bind(size=self._update_text_size)  # change to #2
        SDC_status_container.add_widget(
            self.SDC_status_text_label
        )  # change to #1 and #2

        SDC_status_value = BoxLayout(
            orientation="horizontal", size_hint=(1, 0.6), spacing=5
        )  # 3
        self.SDC_status_value_label = Label(  # change to #3, #4
            text="N/A",
            font_size="45sp",
            halign="left",
            valign="middle",
            size_hint_x=0.4,
            width=160,
            color=(1, 1, 1, 1),
        )
        self.SDC_status_value_label.bind(size=self._update_text_size)  # change to #4
        SDC_status_value.add_widget(self.SDC_status_value_label)
        SDC_status_container.add_widget(SDC_status_value)
        middle_content.add_widget(SDC_status_container)

        left_content = OutlinedBox(
            orientation="vertical", spacing=5, size_hint=(0.33, 1)
        )

        ## Middle section layout

        cell_max_temp_container = BoxLayout(
            orientation="vertical", spacing=5, size_hint=(1, 0.2)
        )  # change #1
        self.cell_max_temp_text_label = Label(  # 2
            text="Cell Max",
            font_size="40sp",
            halign="left",
            valign="middle",
            size_hint=(1, 0.2),
            color=(0, 1, 1, 1),
        )
        self.cell_max_temp_text_label.bind(size=self._update_text_size)  # change to #2
        cell_max_temp_container.add_widget(
            self.cell_max_temp_text_label
        )  # change to #1 and #2

        cell_max_value = BoxLayout(orientation="horizontal", size_hint=(1, 0.2))  # 3
        self.cell_max_value_label = Label(  # change to #3, #4
            text="000",
            font_size="45sp",
            halign="left",
            valign="middle",
            size_hint_x=0.7,
            width=160,
            color=(1, 1, 1, 1),
        )
        self.cell_max_value_label.bind(size=self._update_text_size)  # change to #4
        cell_max_value.add_widget(self.cell_max_value_label)
        self.cell_max_temp_unit_label = Label(
            text="°C",
            font_size="45sp",
            halign="left",
            valign="middle",
            size_hint_x=2,
            width=60,
            color=(1, 1, 1, 1),
        )
        self.cell_max_temp_unit_label.bind(size=self._update_text_size)
        cell_max_value.add_widget(self.cell_max_temp_unit_label)
        cell_max_temp_container.add_widget(cell_max_value)
        left_content.add_widget(cell_max_temp_container)

        # Cell max temp-container
        cell_min_temp_container = BoxLayout(
            orientation="vertical", spacing=5, size_hint=(1, 0.2)
        )
        self.cell_min_temp_text_label = Label(
            text="Cell Min",
            font_size="40sp",
            halign="left",
            valign="middle",
            size_hint=(1, 0.4),
            color=(0, 1, 1, 1),
        )
        self.cell_min_temp_text_label.bind(size=self._update_text_size)
        cell_min_temp_container.add_widget(
            self.cell_min_temp_text_label
        )  # change to #1 and #2

        cell_min_value = BoxLayout(
            orientation="horizontal", size_hint=(1, 0.33), spacing=5
        )  # 3
        self.cell_min_value_label = Label(  # change to #3, #4
            text="000",
            font_size="45sp",
            halign="left",
            valign="middle",
            size_hint_x=0.7,
            width=160,
            color=(1, 1, 1, 1),
        )
        self.cell_min_value_label.bind(size=self._update_text_size)  # change to #4
        cell_min_value.add_widget(self.cell_min_value_label)
        self.cell_min_temp_unit_label = Label(
            text="°C",
            font_size="45sp",
            halign="left",
            valign="middle",
            size_hint_x=2,
            width=60,
            color=(1, 1, 1, 1),
        )
        self.cell_min_temp_unit_label.bind(size=self._update_text_size)
        cell_min_value.add_widget(self.cell_min_temp_unit_label)
        cell_min_temp_container.add_widget(cell_min_value)
        left_content.add_widget(cell_min_temp_container)

        # LV-bat temp-container

        pack_current_container = BoxLayout(
            orientation="vertical", size_hint=(1, 0.2)
        )  # 1/3 av vänster sida
        self.Pack_Current_text_label = Label(
            text="Pack Current",
            font_size="40sp",
            halign="left",
            valign="middle",
            size_hint=(1, 0.4),
            color=(0, 1, 1, 1),
        )
        self.Pack_Current_text_label.bind(size=self._update_text_size)
        pack_current_container.add_widget(self.Pack_Current_text_label)

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
        pack_current_container.add_widget(current_value_layout)
        left_content.add_widget(pack_current_container)

        pack_soc_container = BoxLayout(
            orientation="vertical", spacing=5, size_hint=(1, 0.2)
        )  # change #1
        self.pack_soc_text_label = Label(  # 2
            text="Pack SOC",
            font_size="40sp",
            halign="left",
            valign="middle",
            size_hint=(1, 0.4),
            color=(0, 1, 1, 1),
        )
        self.pack_soc_text_label.bind(size=self._update_text_size)  # change to #2
        pack_soc_container.add_widget(self.pack_soc_text_label)  # change to #1 and #2

        soc_value_layout = BoxLayout(
            orientation="horizontal", size_hint=(1, 0.6), spacing=5
        )  # 3
        self.soc_value_label = Label(  # change to #3, #4
            text="000",
            font_size="45sp",
            halign="left",
            valign="middle",
            size_hint_x=0.7,
            width=160,
            color=(1, 1, 1, 1),
        )
        self.soc_value_label.bind(size=self._update_text_size)  # change to #4
        soc_value_layout.add_widget(self.soc_value_label)
        self.soc_unit_label = Label(
            text="%",
            font_size="45sp",
            halign="left",
            valign="middle",
            size_hint_x=2,
            width=80,
            color=(1, 1, 1, 1),
        )
        self.soc_unit_label.bind(size=self._update_text_size)
        soc_value_layout.add_widget(self.soc_unit_label)
        pack_soc_container.add_widget(soc_value_layout)
        left_content.add_widget(pack_soc_container)

        pack_voltage_container = BoxLayout(
            orientation="vertical", spacing=5, size_hint=(1, 0.2)
        )
        self.pack_voltage_text_label = Label(
            text="Pack Voltage",
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

        # Höger innehåll: Fel- och varningssektioner (placeras högerut)
        right_content = OutlinedBox(
            orientation="vertical", spacing=5, size_hint=(0.33, 1)
        )

        error_section = BoxLayout(orientation="vertical", size_hint=(1, 0.2))
        error_title_layout = BoxLayout(orientation="horizontal", size_hint=(1, 0.2))
        self.errors_label = Label(
            text="TSCU Errors",
            font_size="40sp",
            halign="left",
            valign="middle",
            size_hint_x=0.2,
            color=(0, 1, 1, 1),
        )
        error_title_layout.add_widget(self.errors_label)
        self.errors_label.bind(size=self._update_text_size)

        error_amount = BoxLayout(
            orientation="horizontal", size_hint=(1, 0.2)
        )  # 3
        self.error_amount_label = Label(  # change to #3, #4
            text="0",
            font_size="45sp",
            halign="left",
            valign="middle",
            size_hint_x=0.7,
            color=(1, 1, 1, 1),
        )
        self.error_amount_label.bind(size=self._update_text_size)  # change to #4

        error_section.add_widget(error_title_layout)
        right_content.add_widget(error_section)
        error_amount.add_widget(self.error_amount_label)
        error_section.add_widget(error_amount)

        # LV-bat temp-container
        tsact_status_container = BoxLayout(
            orientation="vertical", size_hint=(1, 0.2)
        )  # change #1
        self.tsact_status_text_label = Label(  # 2
            text="TSACT",
            font_size="40sp",
            halign="left",
            valign="middle",
            size_hint=(1, 0.2),
            color=(0, 1, 1, 1),
        )
        self.tsact_status_text_label.bind(size=self._update_text_size)  # change to #2
        tsact_status_container.add_widget(
            self.tsact_status_text_label
        )  # change to #1 and #2

        tsact_status = BoxLayout(
            orientation="horizontal", size_hint=(1, 0.2), spacing=5
        )  # 3
        self.tsact_status_label = Label(  # change to #3, #4
            text="HIGH",
            font_size="45sp",
            halign="left",
            valign="middle",
            size_hint_x=0.7,
            width=160,
            color=(1, 1, 1, 1),
        )
        self.tsact_status_label.bind(size=self._update_text_size)  # change to #4
        tsact_status.add_widget(self.tsact_status_label)
        tsact_status_container.add_widget(tsact_status)
        right_content.add_widget(tsact_status_container)

        pre_status_container = BoxLayout(
            orientation="vertical", spacing=5, size_hint=(1, 0.2)
        )  # change #1
        self.pre_status_text_label = Label(  # 2
            text="PRE",
            font_size="40sp",
            halign="left",
            valign="middle",
            size_hint=(1, 0.2),
            color=(0, 1, 1, 1),
        )
        self.pre_status_text_label.bind(size=self._update_text_size)  # change to #2
        pre_status_container.add_widget(
            self.pre_status_text_label
        )  # change to #1 and #2

        pre_value = BoxLayout(
            orientation="horizontal", size_hint=(1, 0.2), spacing=5
        )  # 3
        self.pre_value_label = Label(  # change to #3, #4
            text="0",
            font_size="45sp",
            halign="left",
            valign="middle",
            size_hint_x=0.7,
            width=160,
            color=(1, 1, 1, 1),
        )
        self.pre_value_label.bind(size=self._update_text_size)  # change to #4
        pre_value.add_widget(self.pre_value_label)
        pre_status_container.add_widget(pre_value)

        right_content.add_widget(pre_status_container)

        inv95p_status_container = BoxLayout(
            orientation="vertical", spacing=5, size_hint=(1, 0.2)
        )  # change #1
        self.inv95p_value_text_label = Label(  # 2
            text="INV95P",
            font_size="40sp",
            halign="left",
            valign="middle",
            size_hint=(1, 0.4),
            color=(0, 1, 1, 1),
        )
        self.inv95p_value_text_label.bind(size=self._update_text_size)  # change to #2
        inv95p_status_container.add_widget(
            self.inv95p_value_text_label
        )  # change to #1 and #2

        inv95p_value = BoxLayout(
            orientation="horizontal", size_hint=(1, 0.5), spacing=5
        )  # 3
        self.inv95p_value_label = Label(  # change to #3, #4
            text="0",
            font_size="45sp",
            halign="left",
            valign="middle",
            size_hint_x=0.7,
            width=160,
            color=(1, 1, 1, 1),
        )
        self.inv95p_value_label.bind(size=self._update_text_size)  # change to #4
        inv95p_value.add_widget(self.inv95p_value_label)
        inv95p_status_container.add_widget(inv95p_value)

        right_content.add_widget(inv95p_status_container)

        LV_bat_container = BoxLayout(
            orientation="vertical", spacing=5, size_hint=(1, 0.2)
        )  # change #1
        self.lv_bat_voltage_text_label = Label(  # 2
            text="LV Bat Volt",
            font_size="40sp",
            halign="left",
            valign="middle",
            size_hint=(1, 0.3),
            color=(0, 1, 1, 1),
        )
        self.lv_bat_voltage_text_label.bind(size=self._update_text_size)  # change to #2
        LV_bat_container.add_widget(
            self.lv_bat_voltage_text_label
        )  # change to #1 and #2

        lv_bat_value = BoxLayout(
            orientation="horizontal", size_hint=(1, 0.5), spacing=5
        )  # 3
        self.lv_bat_value_label = Label(  # change to #3, #4
            text="000",
            font_size="40sp",
            halign="left",
            valign="middle",
            size_hint_x=0.7,
            width=160,
            color=(1, 1, 1, 1),
        )
        self.lv_bat_value_label.bind(size=self._update_text_size)  # change to #4
        lv_bat_value.add_widget(self.lv_bat_value_label)
        self.lv_bat_unit_label = Label(
            text="V",
            font_size="45sp",
            halign="left",
            valign="middle",
            size_hint_x=2,
            width=60,
            color=(1, 1, 1, 1),
        )
        self.lv_bat_unit_label.bind(size=self._update_text_size)
        lv_bat_value.add_widget(self.lv_bat_unit_label)
        LV_bat_container.add_widget(lv_bat_value)
        right_content.add_widget(LV_bat_container)


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
        # Uppdatera temperaturer
        self.tscu_state_label.text = f"{self.SharedData.tscu_state}"
        self.tscu_mode_label.text = f"{self.SharedData.tscu_mode}"
        self.airplus_state_label.text = f"{self.SharedData.airplus_state}"
        self.airminus_state_label.text = f"{self.SharedData.airminus_state}"
        self.tsact_status_label.text = f"{self.SharedData.tsact}"
        self.inv95p_value_label.text = f"{self.SharedData.inv95p}"
        self.SDC_status_value_label.text = f"{self.SharedData.sdc}"
        self.pre_value_label.text = f"{self.SharedData.pre}"

        #LV BAT
        self.lv_bat_value_label.text = f"{self.SharedData.lvvoltage}"

        if self.SharedData.tscu_fault:
            self.error_amount_label.text = "N/A"
        else:
            error_count = len(self.SharedData.tscu_errors)
            self.error_amount_label.text = f"{error_count}"


        if self.SharedData.orionpower_fault:
            self.current_value_value_label.text = "N/A"
            self.soc_value_label.text = "N/A"
            self.voltage_value_label.text = "N/A"
        else:
            self.current_value_value_label.text = f"{self.SharedData.orioncurrent}"
            self.soc_value_label.text = f"{self.SharedData.orionsoc}"
            self.voltage_value_label.text = f"{self.SharedData.orionvoltage}"

        self.cell_min_value_label.text = f"{self.SharedData.packtemp_min}"
        self.cell_max_value_label.text = f"{self.SharedData.packtemp_max}"


    def _update_separator(self, instance, value):
        # Update the separator line's points based on the widget's current position and size
        self.separator_line.points = [
            instance.x,
            instance.y + instance.height / 2,
            instance.x + instance.width,
            instance.y + instance.height / 2,
        ]


class TSACApp(App):
    def build(self):
        return TSAC()


if __name__ == "__main__":
    TSAC().run()
