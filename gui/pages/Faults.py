from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import Screen
from kivy.core.window import Window
from kivy.graphics import Color, Line
from kivy.uix.image import Image
import os

from gui.shared_data import SharedDataDriver
from gui.widgets import OutlinedBox


class Faults(Screen):
    def __init__(self, **kwargs):
        super(Faults, self).__init__(**kwargs)
        self.SharedData = SharedDataDriver()

        root_layout = BoxLayout(orientation="vertical")

        header_layout = BoxLayout(orientation="horizontal", size_hint=(1, 0.15))
        self.debug_label = Label(text="Debug", font_size="70sp", size_hint_x=0.3, color=(0, 1, 1, 1))
        image_path = os.path.join("./gui/images/logo.png")
        self.logo_image = Image(source=image_path, opacity=0.15, allow_stretch=True, keep_ratio=True, size_hint_x=0.4)
        self.fault_label = Label(text="FAULTS", font_size="70sp", size_hint_x=0.3, color=(0, 1, 1, 1))
        header_layout.add_widget(self.debug_label)
        header_layout.add_widget(self.logo_image)
        header_layout.add_widget(self.fault_label)

        separator = Widget(size_hint=(1, None), height=5)
        with separator.canvas:
            Color(1, 1, 2, 0.5)
            self.separator_line = Line(points=[], width=8)
        separator.bind(pos=self._update_separator, size=self._update_separator)

        root_layout.add_widget(header_layout)
        root_layout.add_widget(separator)
        main_layout = BoxLayout(orientation="horizontal", spacing=10)
        root_layout.add_widget(main_layout)

        # CUSTOM ERRORS
        left_section = OutlinedBox(orientation="vertical", spacing=10, size_hint=(0.33, 1))
        custom_title_layout = BoxLayout(orientation="horizontal", size_hint=(1, 0.1), spacing=10)
        self.custom_errors_label = Label(text="Errors", font_size="45sp", size_hint_x=0.7, color=(0, 1, 1, 1))
        self.custom_errors_amount_label = Label(text="(0)", font_size="45sp", size_hint_x=0.5, color=(0, 1, 1, 1))
        custom_title_layout.add_widget(self.custom_errors_label)
        custom_title_layout.add_widget(self.custom_errors_amount_label)
        left_section.add_widget(custom_title_layout)
        self.scroll_view_custom_errors = ScrollView(size_hint=(1, 0.8), do_scroll_x=False)
        self.custom_errors_content_layout = BoxLayout(orientation="vertical", spacing=10, size_hint_y=None)
        self.custom_errors_content_layout.bind(minimum_height=self.custom_errors_content_layout.setter("height"))
        self.scroll_view_custom_errors.add_widget(self.custom_errors_content_layout)
        left_section.add_widget(self.scroll_view_custom_errors)
        main_layout.add_widget(left_section)

        # TSCU ERRORS
        middle_section = OutlinedBox(orientation="vertical", spacing=10, size_hint=(0.33, 1))
        tscu_section = BoxLayout(orientation="vertical", spacing=20, size_hint=(1, 0.4))
        tscu_title_layout = BoxLayout(orientation="horizontal", size_hint=(1, 0.1), spacing=10)
        self.tscu_errors_label = Label(text="TSCU ERRORS", font_size="40sp", size_hint=(0.2, 1), color=(0, 1, 1, 1))
        self.tscu_errors_amount_label = Label(text="(0)", font_size="40sp", size_hint=(0.05, 1), color=(0, 1, 1, 1))
        tscu_title_layout.add_widget(self.tscu_errors_label)
        tscu_title_layout.add_widget(self.tscu_errors_amount_label)
        tscu_section.add_widget(tscu_title_layout)
        self.scroll_view_tscu = ScrollView(size_hint=(1, 0.8), do_scroll_x=False, do_scroll_y=True)
        self.tscu_errors_content_layout = BoxLayout(orientation="vertical", spacing=10, size_hint_y=None)
        self.tscu_errors_content_layout.bind(minimum_height=self.tscu_errors_content_layout.setter("height"))
        self.scroll_view_tscu.add_widget(self.tscu_errors_content_layout)
        tscu_section.add_widget(self.scroll_view_tscu)
        middle_section.add_widget(tscu_section)
        main_layout.add_widget(middle_section)

        # INV ERRORS
        right_section = OutlinedBox(orientation="vertical", spacing=10, size_hint=(0.33, 1))
        inv_section = BoxLayout(orientation="vertical", spacing=20, size_hint=(1, 0.4))
        inv_title_layout = BoxLayout(orientation="horizontal", size_hint=(1, 0.1), spacing=10)
        self.inv_errors_label = Label(text="INV ERRORS", font_size="40sp", size_hint=(0.2, 1), color=(0, 1, 1, 1))
        self.inv_errors_amount_label = Label(text="(0)", font_size="40sp", size_hint=(0.05, 1), color=(0, 1, 1, 1))
        inv_title_layout.add_widget(self.inv_errors_label)
        inv_title_layout.add_widget(self.inv_errors_amount_label)
        inv_section.add_widget(inv_title_layout)
        self.scroll_view_inv = ScrollView(size_hint=(1, 0.8), do_scroll_x=False, do_scroll_y=True)
        self.inv_errors_content_layout = BoxLayout(orientation="vertical", spacing=10, size_hint_y=None)
        self.inv_errors_content_layout.bind(minimum_height=self.inv_errors_content_layout.setter("height"))
        self.scroll_view_inv.add_widget(self.inv_errors_content_layout)
        inv_section.add_widget(self.scroll_view_inv)
        right_section.add_widget(inv_section)
        main_layout.add_widget(right_section)

        # Preallocate label widgets (8 per section)
        self.custom_error_labels = self._create_error_labels(self.custom_errors_content_layout)
        self.tscu_error_labels = self._create_error_labels(self.tscu_errors_content_layout)
        self.inv_error_labels = self._create_error_labels(self.inv_errors_content_layout)

        self.add_widget(root_layout)

    def _create_error_labels(self, layout):
        labels = []
        for _ in range(8):
            lbl = Label(text="", font_size="25sp", size_hint_y=None, height=50,
                        halign="center", valign="middle", color=(1, 1, 1, 1))
            lbl.bind(size=self._update_text_size)
            layout.add_widget(lbl)
            labels.append(lbl)
        return labels

    def refresh(self):
        # Custom errors
        custom_errors = list(self.SharedData.faults)
        self.custom_errors_amount_label.text = f"({len(custom_errors)})"
        for i in range(8):
            if i < len(custom_errors):
                error = custom_errors[i]
                display_error = error[1:] if error.startswith(".") else error
                color = (1, 0.5, 0, 1) if error.startswith(".") else (1, 0, 0, 1)
                self.custom_error_labels[i].text = display_error
                self.custom_error_labels[i].color = color
            else:
                self.custom_error_labels[i].text = ""

        # TSCU errors
        tscu_errors = list(self.SharedData.tscu_errors)
        self.tscu_errors_amount_label.text = f"({len(tscu_errors)})"
        for i in range(8):
            if i < len(tscu_errors):
                self.tscu_error_labels[i].text = tscu_errors[i]
                self.tscu_error_labels[i].color = (1, 0, 0, 1)
            else:
                self.tscu_error_labels[i].text = ""

        # INV errors
        inv_errors = list(self.SharedData.inv_errors + self.SharedData.inv_warnings)
        self.inv_errors_amount_label.text = f"({len(inv_errors)})"
        for i in range(8):
            if i < len(inv_errors):
                self.inv_error_labels[i].text = inv_errors[i]
                self.inv_error_labels[i].color = (1, 0, 0, 1)
            else:
                self.inv_error_labels[i].text = ""

    def _update_text_size(self, instance, value):
        instance.text_size = (instance.width, None)

    def _update_separator(self, instance, value):
        self.separator_line.points = [
            instance.x, instance.y + instance.height / 2,
            instance.x + instance.width, instance.y + instance.height / 2
        ]


class FaultsApp(App):
    def build(self):
        return Faults()


if __name__ == "__main__":
    FaultsApp().run()