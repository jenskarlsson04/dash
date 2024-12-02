from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle
from kivy.properties import StringProperty


class StatusBar(Widget):
    status_text = StringProperty("Disconnected")  # Default status

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(status_text=self.update_color)  # Update color when status changes

        # Draw the bar and add the label
        self.draw_bar()
        self.add_status_label()

    def draw_bar(self):
        """Draw the bar with the initial color."""
        with self.canvas:
            # Set initial color (red for Disconnected)
            self.color = Color(1, 0, 0, 1)  # Default color is red
            self.bar = Rectangle(pos=self.pos, size=(self.width, 50))

        self.bind(pos=self.update_bar, size=self.update_bar)

    def add_status_label(self):
        """Add the status label in the middle of the bar."""
        self.status_label = Label(
            text=self.status_text,
            size_hint=(None, None),
            font_size=18,
            halign="center",
            valign="middle",
            color=(1, 1, 1, 1),  # White text
        )
        self.update_label_position()
        self.add_widget(self.status_label)

    def update_bar(self, *args):
        """Update the bar's position and size."""
        self.bar.pos = self.pos
        self.bar.size = (self.width, 50)
        self.update_label_position()

    def update_label_position(self):
        """Update the label's position to keep it centered."""
        self.status_label.pos = (
            self.x + (self.width - self.status_label.width) / 2,
            self.y + (50 - self.status_label.height) / 2,
        )

    def update_color(self, *args):
        """Change the bar's color and update the label text."""
        if self.status_text == "Systems Connected":
            self.color.rgb = (0, 1, 0)  # Green
        else:
            self.color.rgb = (1, 0, 0)  # Red

        # Update the label text
        self.status_label.text = self.status_text


class StatusBarApp(App):
    def build(self):
        layout = BoxLayout(orientation="vertical")

        # Create the status bar
        self.status_bar = StatusBar(size_hint=(1, None), height=50)
        layout.add_widget(self.status_bar)

        # Add buttons to change the status
        from kivy.uix.button import Button

        btn_connected = Button(text="Set to Connected")
        btn_connected.bind(on_press=lambda x: self.set_status("Systems Connected"))
        layout.add_widget(btn_connected)

        btn_disconnected = Button(text="Set to Disconnected")
        btn_disconnected.bind(on_press=lambda x: self.set_status("Disconnected"))
        layout.add_widget(btn_disconnected)

        return layout

    def set_status(self, status):
        """Set the status text and update the bar."""
        self.status_bar.status_text = status


if __name__ == "__main__":
    StatusBarApp().run()
