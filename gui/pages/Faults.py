# Fil med alla felkoder från .shared_data och från inverter och tscu

import random
import os
from kivy.uix.image import Image

# Import kivy
from kivy.uix.scrollview import ScrollView
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup
from kivy.core.window import Window
from kivy.graphics import Color, Line

# Import Custom widgets
from gui.widgets import OutlinedBox

# Import can stuff

# Import error messages and CAN data
from gui.shared_data import SharedDataDriver


class DismissablePopup(Popup):
    """
    A custom popup that dismisses when the "o" key is pressed.
    """

    def on_open(self):
        # Request the keyboard when the popup opens.
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        if self._keyboard:
            self._keyboard.bind(on_key_down=self._on_keyboard_down)

    def on_dismiss(self):
        # Unbind and release the keyboard when the popup is dismissed.
        if hasattr(self, "_keyboard") and self._keyboard:
            self._keyboard.unbind(on_key_down=self._on_keyboard_down)
            self._keyboard = None

    def _keyboard_closed(self):
        if hasattr(self, "_keyboard") and self._keyboard:
            self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        # Dismiss the popup when the "o" key is pressed.
        if keycode[1] == "o":
            self.dismiss()
        return True


# Main Dashboard Page
class Faults(Screen):
    def __init__(self, **kwargs):
        super(Faults, self).__init__(**kwargs)
        self.SharedData = SharedDataDriver()

        root_layout = BoxLayout(orientation="vertical")

        # Use a main layout to contain the dashboard elements

        header_layout = BoxLayout(orientation="horizontal", size_hint=(1, 0.15))
        #       DEBUG TEXT
        self.debug_label = Label(
            text="Debug",
            font_size="70sp",
            size_hint_x=0.3,
            color=(0, 1, 1, 1),
            halign="left",
            valign="middle",
        )

        # LOGO

        image_path = os.path.join("./gui/images/logo.png")
        self.logo_image = Image(
            source=image_path,
            opacity=0.15,
            allow_stretch=True,
            keep_ratio=True,
            size_hint_x=0.4,
        )

        # FAULTS TEXT

        self.fault_label = Label(
            text="FAULTS",
            font_size="70sp",
            size_hint_x=0.3,
            color=(0, 1, 1, 1),
            halign="right",
            valign="middle",
        )
        header_layout.add_widget(self.debug_label)
        header_layout.add_widget(self.logo_image)
        header_layout.add_widget(self.fault_label)

        #        LINE SEPERATOR
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

        left_section = OutlinedBox(
            orientation="vertical", spacing=10, size_hint=(0.33, 1)
        )

        custom_error_title_layout = BoxLayout(
            orientation="horizontal", size_hint=(1, 0.1), spacing=10
        )
        self.custom_errors_label = Label(
            text="Errors",
            font_size="45sp",
            halign="center",
            valign="middle",
            size_hint_x=0.7,
            color=(0, 1, 1, 1),
        )
        custom_error_title_layout.add_widget(self.custom_errors_label)
        self.custom_errors_amount_label = Label(
            text="(0)",
            font_size="45sp",
            halign="left",
            valign="middle",
            size_hint_x=0.5,
            color=(0, 1, 1, 1),
        )
        custom_error_title_layout.add_widget(self.custom_errors_amount_label)
        left_section.add_widget(custom_error_title_layout)

        self.scroll_view_custom_errors = ScrollView(
            size_hint=(1, 0.8), do_scroll_x=False, do_scroll_y=False
        )
        self.custom_errors_content_layout = BoxLayout(
            orientation="vertical", spacing=10, size_hint_y=None
        )
        self.custom_errors_content_layout.bind(
            minimum_height=self.custom_errors_content_layout.setter("height")
        )
        self.scroll_view_custom_errors.add_widget(self.custom_errors_content_layout)
        left_section.add_widget(self.scroll_view_custom_errors)

        main_layout.add_widget(left_section)

        # TSCU ERRORS

        middle_section = OutlinedBox(
            orientation="vertical", spacing=10, size_hint=(0.33, 1)
        )

        tscu_error_section = BoxLayout(
            orientation="vertical", spacing=20, size_hint=(1, 0.4)
        )
        tscu_error_title_layout = BoxLayout(
            orientation="horizontal", size_hint=(1, 0.1), spacing=10
        )
        self.tscu_errors_label = Label(
            text="TSCU ERRORS",
            font_size="40sp",
            halign="center",
            valign="middle",
            size_hint=(0.2, 1),
            color=(0, 1, 1, 1),
        )
        tscu_error_title_layout.add_widget(self.tscu_errors_label)
        self.tscu_errors_amount_label = Label(
            text="(0)",
            font_size="40sp",
            halign="left",
            valign="middle",
            size_hint=(0.05, 1),
            color=(0, 1, 1, 1),
        )
        tscu_error_title_layout.add_widget(self.tscu_errors_amount_label)
        tscu_error_section.add_widget(tscu_error_title_layout)

        self.scroll_view_errors = ScrollView(
            size_hint=(1, 0.8), do_scroll_x=False, do_scroll_y=True
        )
        self.tscu_errors_content_layout = BoxLayout(
            orientation="vertical",
            spacing=10,
            size_hint_y=None,
        )
        self.tscu_errors_content_layout.bind(
            minimum_height=self.tscu_errors_content_layout.setter("height")
        )

        self.scroll_view_errors.add_widget(self.tscu_errors_content_layout)
        tscu_error_section.add_widget(self.scroll_view_errors)

        middle_section.add_widget(tscu_error_section)

        main_layout.add_widget(middle_section)

        # Right section
        right_section = OutlinedBox(
            orientation="vertical", spacing=10, size_hint=(0.33, 1)
        )

        # INV ERRORS

        error_section = BoxLayout(
            orientation="vertical", spacing=20, size_hint=(1, 0.4)
        )
        error_title_layout = BoxLayout(
            orientation="horizontal", size_hint=(1, 0.1), spacing=10
        )
        self.inv_errors_label = Label(
            text="INV ERRORS",
            font_size="40sp",
            halign="center",
            valign="middle",
            size_hint=(0.2, 1),
            color=(0, 1, 1, 1),
        )
        error_title_layout.add_widget(self.inv_errors_label)
        self.inv_errors_amount_label = Label(
            text="(0)",
            font_size="40sp",
            halign="left",
            valign="middle",
            size_hint=(0.05, 1),
            color=(0, 1, 1, 1),
        )
        error_title_layout.add_widget(self.inv_errors_amount_label)
        error_section.add_widget(error_title_layout)

        self.scroll_view_errors = ScrollView(
            size_hint=(1, 0.8), do_scroll_x=False, do_scroll_y=True
        )
        self.inv_errors_content_layout = BoxLayout(
            orientation="vertical",
            spacing=10,
            size_hint_y=None,
        )
        self.inv_errors_content_layout.bind(
            minimum_height=self.inv_errors_content_layout.setter("height")
        )

        self.scroll_view_errors.add_widget(self.inv_errors_content_layout)
        error_section.add_widget(self.scroll_view_errors)

        right_section.add_widget(error_section)
        main_layout.add_widget(right_section)

        self.add_widget(root_layout)

    def refresh(self):

        # Custom errors
        custom_error_count = len(self.SharedData.faults)
        self.custom_errors_amount_label.text = f"({custom_error_count})"
        self.custom_errors_content_layout.clear_widgets()
        custom_errors_to_show = list(self.SharedData.faults)

        for i, custom_error in enumerate(custom_errors_to_show[:8]):
            if custom_error.startswith("."):
                custom_display_error = custom_error[1:]  # Remove the leading dot
                custom_error_color = (1, 0.5, 0, 1)  # Orange
            else:
                custom_display_error = custom_error
                custom_error_color = (1, 0, 0, 1)  # Red

            label = Label(
                text=custom_display_error,
                font_size="25sp",
                size_hint_y=None,
                height=50,
                halign="center",
                valign="middle",
                color=custom_error_color,
            )
            label.bind(size=self._update_text_size)
            self.custom_errors_content_layout.add_widget(label)

            if i < len(custom_errors_to_show) - 1:
                spacer = Widget(size_hint_y=None, height=0)
                self.custom_errors_content_layout.add_widget(spacer)

        # INV ERRORS AND WARNINGS

        inv_fault_count = len(self.SharedData.inv_errors + self.SharedData.inv_warnings)
        self.inv_errors_amount_label.text = f"({inv_fault_count})"
        self.inv_errors_content_layout.clear_widgets()
        inv_faults_to_show = list(
            self.SharedData.inv_errors + self.SharedData.inv_warnings
        )

        for i, error in enumerate(inv_faults_to_show[:8]):
            label = Label(
                text=error,
                font_size="25sp",
                size_hint_y=None,
                height=50,  # increased height for better spacing
                halign="center",
                valign="middle",
                color=(1, 0, 0, 1),
            )
            label.bind(size=self._update_text_size)
            self.inv_errors_content_layout.add_widget(label)
            if i < len(inv_faults_to_show) - 1:
                inv_spacer = Widget(size_hint_y=None, height=0)
                self.inv_errors_content_layout.add_widget(inv_spacer)

        # TSCU faults
        tscu_fault_count = len(self.SharedData.tscu_errors)
        self.tscu_errors_amount_label.text = f"({tscu_fault_count})"
        self.tscu_errors_content_layout.clear_widgets()
        tscu_faults_to_show = list(self.SharedData.tscu_errors)

        for i, error in enumerate(tscu_faults_to_show[:8]):
            label = Label(
                text=error,
                font_size="25sp",
                size_hint_y=None,
                height=50,  # increased height for better spacing
                halign="center",
                valign="middle",
                color=(1, 0, 0, 1),
            )
            label.bind(size=self._update_text_size)
            self.tscu_errors_content_layout.add_widget(label)
            if i < len(tscu_faults_to_show) - 1:
                tscu_spacer = Widget(size_hint_y=None, height=0)
                self.tscu_errors_content_layout.add_widget(tscu_spacer)

    def _update_text_size(self, instance, value):
        # Set text_size to the width only so the text does not wrap vertically
        instance.text_size = (instance.width, None)

    def _update_separator(self, instance, value):
        # Update the separator line's points based on the widget's current position and size
        self.separator_line.points = [
            instance.x,
            instance.y + instance.height / 2,
            instance.x + instance.width,
            instance.y + instance.height / 2,
        ]


# Main App Class
class FaultsApp(App):
    def build(self):
        return Faults()


if __name__ == "__main__":
    FaultsApp().run()
