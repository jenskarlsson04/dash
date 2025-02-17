import os
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, Rectangle
from kivy.clock import Clock
from kivy.core.window import Window


class DriverDashboard(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Bakgrundsfärg
        with self.canvas.before:
            Color(0, 0, 0, 1)  # Svart bakgrund
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self.update_rect, pos=self.update_rect)

        # LOGO och TITEL
        self.add_widget(Label(text="[Logo]", font_size="40sp", color=(1, 1, 1, 0.5),
                              pos_hint={"center_x": 0.5, "center_y": 0.9}))
        self.add_widget(Label(text="Orion", font_size="35sp", color=(0.5, 0.8, 1, 1),
                              pos_hint={"center_x": 0.5, "center_y": 0.85}))

        # VÄRDEDATA (vänster kolumn)
        self.pack_current_label = self.create_data_label("PACK CURRENT", "0.00 A", 0.2, 0.75)
        self.pack_volt_label = self.create_data_label("PACK VOLT", "000 V", 0.2, 0.65)
        self.pack_soc_label = self.create_data_label("PACK SOC", "0.00 %", 0.2, 0.55)
        self.max_cell_temp_label = self.create_data_label("MAX CELL TEMP", "000 C", 0.2, 0.45)
        self.min_cell_temp_label = self.create_data_label("MIN CELL TEMP", "000 C", 0.2, 0.35)

        # VÄRDEDATA (höger kolumn)
        self.max_cell_volt_label = self.create_data_label("MAX CELL VOLT", "000 V", 0.7, 0.75)
        self.min_cell_volt_label = self.create_data_label("MIN CELL VOLT", "000 V", 0.7, 0.65)

        # SYSTEMSTATUS (längst ner)
        self.system_status_label = Label(
            text="Systems: Connected",
            font_size="20sp",
            bold=True,
            color=(0, 1, 0, 1),
            pos_hint={"center_x": 0.5, "center_y": 0.1}
        )
        self.add_widget(self.system_status_label)

        # Simulera uppdatering av värden
        Clock.schedule_interval(self.update_values, 1)

    def update_rect(self, *args):
        """Uppdatera bakgrundens storlek och position."""
        self.rect.size = self.size
        self.rect.pos = self.pos

    def create_data_label(self, title, value, x, y):
        """Skapa en etikett för en datapunkt."""
        self.add_widget(Label(text=title, font_size="18sp", color=(0.5, 0.8, 1, 1),
                              pos_hint={"center_x": x, "center_y": y + 0.05}))
        value_label = Label(text=value, font_size="20sp", color=(1, 1, 1, 1),
                            pos_hint={"center_x": x, "center_y": y})
        self.add_widget(value_label)
        return value_label

    def update_values(self, dt):
        """Simulera och uppdatera dashboardvärden."""
        # Simulerade värden
        pack_current = round(10 * (1 - 0.5), 2)
        pack_volt = 240
        max_cell_volt = 4.2
        min_cell_volt = 3.5
        pack_soc = 85.5
        max_cell_temp = 40
        min_cell_temp = 22

        # Uppdatera etiketter
        self.pack_current_label.text = f"{pack_current:.2f} A"
        self.pack_volt_label.text = f"{pack_volt} V"
        self.max_cell_volt_label.text = f"{max_cell_volt:.2f} V"
        self.min_cell_volt_label.text = f"{min_cell_volt:.2f} V"
        self.pack_soc_label.text = f"{pack_soc:.2f} %"
        self.max_cell_temp_label.text = f"{max_cell_temp} C"
        self.min_cell_temp_label.text = f"{min_cell_temp} C"

        # Växla systemstatus
        self.system_status_label.text = "Systems: Connected"
        self.system_status_label.color = (0, 1, 0, 1)


class DashboardApp(App):
    def build(self):
        Window.size = (800, 480)  # Anpassa storlek
        return DriverDashboard()


if __name__ == '__main__':
    DashboardApp().run()
