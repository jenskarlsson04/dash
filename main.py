import kivy
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.progressbar import ProgressBar
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.properties import StringProperty, NumericProperty
from kivy.uix.screenmanager import ScreenManager, Screen


# Main GUI class
class CarMonitorScreen(Screen):
    torque = StringProperty("0000")
    brake_pressure = NumericProperty(0)
    apps1 = NumericProperty(0)
    apps2 = NumericProperty(0)
    motor_temp = NumericProperty(0)
    inverter_temp = NumericProperty(0)
    pi_temp = NumericProperty(0.00)
    battery_temp = NumericProperty(0)
    cool_loop_temp = NumericProperty(22)

    def __init__(self, **kwargs):
        super(CarMonitorScreen, self).__init__(**kwargs)

        # Build layout using Grid
        layout = GridLayout(cols=3, padding=10, spacing=10)

        # Inverter state
        layout.add_widget(Label(text="INVERTER STATE", font_size=20))
        layout.add_widget(Label(text=""))
        layout.add_widget(Label(text="MOTOR TEMP", font_size=20))
        layout.add_widget(Label(text="OFF", font_size=40, color=(0.2, 0.5, 1, 1)))
        layout.add_widget(Label(text=""))
        layout.add_widget(Label(text=f"{self.motor_temp} C", font_size=40))

        # VCU state
        layout.add_widget(Label(text="VCU STATE", font_size=20))
        layout.add_widget(Label(text=""))
        layout.add_widget(Label(text="INVERTER TEMP", font_size=20))
        layout.add_widget(Label(text="START", font_size=40, color=(0.2, 0.5, 1, 1)))
        layout.add_widget(Label(text=""))
        layout.add_widget(Label(text=f"{self.inverter_temp} C", font_size=40))

        # Torque and PI temp
        layout.add_widget(Label(text="TORQUE", font_size=20))
        layout.add_widget(Label(text=""))
        layout.add_widget(Label(text="PI TEMP", font_size=20))
        layout.add_widget(Label(text=self.torque, font_size=40))
        layout.add_widget(Label(text=""))
        layout.add_widget(Label(text=f"{self.pi_temp} C", font_size=40))

        # Brake pressure and APPS
        layout.add_widget(Label(text="BRAKE PRESSURE", font_size=20))
        brake_pressure_bar = ProgressBar(value=self.brake_pressure, max=100, size_hint=(1, 0.2))
        layout.add_widget(brake_pressure_bar)
        layout.add_widget(Label(text=""))
        layout.add_widget(Label(text=f"{self.brake_pressure:03}", font_size=40))
        layout.add_widget(Label(text="APPS1", font_size=20))
        layout.add_widget(Label(text="APPS2", font_size=20))

        # APPS1 and APPS2 ProgressBars
        apps1_bar = ProgressBar(value=self.apps1, max=100, size_hint=(1, 0.2))
        layout.add_widget(apps1_bar)
        apps2_bar = ProgressBar(value=self.apps2, max=100, size_hint=(1, 0.2))
        layout.add_widget(apps2_bar)

        layout.add_widget(Label(text=f"{self.apps1:02}", font_size=40))
        layout.add_widget(Label(text=f"{self.apps2:02}", font_size=40))

        # Footer with Battery and Cool Loop
        layout.add_widget(Label(text="BATTERY", font_size=20))
        layout.add_widget(Label(text=""))
        layout.add_widget(Label(text="COOL LOOP", font_size=20))
        layout.add_widget(Label(text=f"{self.battery_temp} C", font_size=40))
        layout.add_widget(Label(text=""))
        layout.add_widget(Label(text=f"{self.cool_loop_temp} C", font_size=40))

        # Add the layout to the screen
        self.add_widget(layout)


# Main App
class CarMonitorApp(App):
    def build(self):
        screen_manager = ScreenManager()
        screen_manager.add_widget(CarMonitorScreen(name="monitor"))
        return screen_manager


# Running the application
if __name__ == '__main__':
    CarMonitorApp().run()
