from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.config import Config
from kivy.uix.progressbar import ProgressBar
from kivy.graphics import Color, Ellipse
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window

Config.set('graphics', 'width', '1024')
Config.set('graphics', 'height', '620')
Config.write()

class Dashboard(FloatLayout):
    def __init__(self, screen, **kwargs):
        super(Dashboard, self).__init__(**kwargs)

        # Velocity display
        self.add_widget(
            Label(text="VELOCITY", font_size='20sp', color=(0, 0.75, 1, 1),
                  size_hint=(0.3, 0.1), pos_hint={"x": 0.05, "top": 0.95}))
        self.add_widget(
            Label(text="000 kph", font_size='40sp', color=(1, 1, 1, 1),
                  size_hint=(0.3, 0.1), pos_hint={"x": 0.05, "top": 0.85}))

        # State of Charge
        self.add_widget(
            Label(text="STATE OF CHARGE", font_size='20sp', color=(0, 0.75, 1, 1),
                  size_hint=(0.3, 0.05), pos_hint={"x": 0.05, "top": 0.75}))

        # Progress Bar for state of charge (75%)
        progress_bar = ProgressBar(value=75, max=100, size_hint=(0.2, 0.05), pos_hint={"x": 0.05, "top": 0.70})
        self.add_widget(progress_bar)
        self.add_widget(
            Label(text="75%", font_size='18sp', color=(0, 0, 0, 1),
                  size_hint=(0.05, 0.05), pos_hint={"x": 0.26, "top": 0.70}))

        # Battery Power
        self.add_widget(
            Label(text="BATTERY POWER", font_size='20sp', color=(0, 0.75, 1, 1),
                  size_hint=(0.3, 0.05), pos_hint={"x": 0.05, "top": 0.60}))
        self.add_widget(
            Label(text="0.00 kW", font_size='40sp', color=(1, 1, 1, 1),
                  size_hint=(0.3, 0.1), pos_hint={"x": 0.05, "top": 0.50}))

        # Right side (Lap times, Battery, Cool Loop, and Status)
        self.add_widget(
            Label(text="Lap", font_size='20sp', color=(0, 0.75, 1, 1),
                  size_hint=(0.2, 0.05), pos_hint={"x": 0.65, "top": 0.95}))

        # Laps and Times
        laps = [("1", "01:28:04"), ("2", "00:44:67"), ("3", "01:33:70"),
                ("4", "00:11:23"), ("5", "00:42:00")]
        y_pos = 0.85
        for lap, time in laps:
            lap_label = Label(text=lap, font_size='20sp', color=(1, 1, 1, 1),
                              size_hint=(0.1, 0.05), pos_hint={"x": 0.65, "top": y_pos})
            time_label = Label(text=time, font_size='20sp', color=(1, 1, 1, 1),
                               size_hint=(0.1, 0.05), pos_hint={"x": 0.75, "top": y_pos})
            self.add_widget(lap_label)
            self.add_widget(time_label)
            y_pos -= 0.1

        # Battery and Cool Loop temperatures
        self.add_widget(Label(text="BATTERY", font_size='18sp', color=(0, 0.75, 1, 1),
                              size_hint=(0.1, 0.05), pos_hint={"x": 0.65, "top": y_pos}))
        self.add_widget(Label(text="00 C", font_size='18sp', color=(1, 1, 1, 1),
                              size_hint=(0.1, 0.05), pos_hint={"x": 0.75, "top": y_pos}))
        y_pos -= 0.1
        self.add_widget(Label(text="COOL LOOP", font_size='18sp', color=(0, 0.75, 1, 1),
                              size_hint=(0.1, 0.05), pos_hint={"x": 0.65, "top": y_pos}))
        self.add_widget(Label(text="22 C", font_size='18sp', color=(1, 1, 1, 1),
                              size_hint=(0.1, 0.05), pos_hint={"x": 0.75, "top": y_pos}))

        # Switch Button
        switch_btn = Button(text="Switch to Car Layout", size_hint=(0.3, 0.1), pos_hint={"x": 0.35, "top": 0.2},
                            on_press=screen.switch_to_car_layout)
        self.add_widget(switch_btn)


class CarLayoutWidget(FloatLayout):
    def __init__(self, screen, **kwargs):
        super(CarLayoutWidget, self).__init__(**kwargs)
        self.screen = screen

        car_image = Image(source='car_top_view.png', allow_stretch=True, keep_ratio=True, size_hint=(1, 0.9),
                          pos_hint={"center_x": 0.5, "center_y": 0.5})
        self.add_widget(car_image)

        self.add_status_overlays()

        switch_btn = Button(text="Switch to Dashboard", size_hint=(1, 0.1), pos_hint={"x": 0, "y": 0},
                            on_press=self.switch_to_dashboard)
        self.add_widget(switch_btn)

    def add_status_overlays(self):
        with self.canvas.after:
            if self.screen.vcu_status == "connected":
                Color(0, 1, 0, 1)  # Green
            elif self.screen.vcu_status == "fault":
                Color(1, 0.5, 0, 1)  # Orange
            else:
                Color(1, 0, 0, 1)  # Red
            Ellipse(pos=(1000, 700), size=(30, 30))  # VCU position

    def switch_to_dashboard(self, instance):
        self.screen.manager.current = 'dashboard'


class DashboardScreen(Screen):
    def __init__(self, **kwargs):
        super(DashboardScreen, self).__init__(**kwargs)
        self.vcu_status = "fault"
        self.bots_status = "fault"
        self.enertia_status = "fault"
        self.layout = FloatLayout()

        self.dashboard_view = Dashboard(self)
        self.layout.add_widget(self.dashboard_view)

        self.add_widget(self.layout)

    def switch_to_car_layout(self, instance):
        self.manager.current = 'car_layout'


class CarLayoutScreen(Screen):
    def __init__(self, **kwargs):
        super(CarLayoutScreen, self).__init__(**kwargs)
        self.vcu_status = "fault"
        self.bots_status = "ok"
        self.enertia_status = "ok"
        self.layout = CarLayoutWidget(self)
        self.add_widget(self.layout)


class DashboardApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(DashboardScreen(name='dashboard'))
        sm.add_widget(CarLayoutScreen(name='car_layout'))
        return sm


if __name__ == '__main__':
    DashboardApp().run()
