from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Line


class OutlinedBox(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(0.5, 0.5, 0.5, 1)  # Grey color (RGBA)
            self.border = Line(
                rectangle=(self.x, self.y, self.width, self.height), width=2
            )

        # Update border when size or position changes
        self.bind(pos=self.update_border, size=self.update_border)

    def update_border(self, *args):
        self.border.rectangle = (self.x, self.y, self.width, self.height)
