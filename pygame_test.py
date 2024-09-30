from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.progressbar import ProgressBar
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import Screen, ScreenManager


class OverviewScreen(Screen):
    def __init__(self, **kwargs):
        super(OverviewScreen, self).__init__(**kwargs)

        # Create main layout for the screen
        layout = BoxLayout(orientation='horizontal')

        # Left side (Velocity, State of Charge, Battery Power)
        left_box = BoxLayout(orientation='vertical', padding=20, spacing=20)

        # Velocity display
        left_box.add_widget(
            Label(text="VELOCITY", font_size='20sp', color=(0, 0.75, 1, 1), halign='left', size_hint_y=None, height=50))
        left_box.add_widget(
            Label(text="000 kph", font_size='40sp', color=(1, 1, 1, 1), halign='left', size_hint_y=None, height=100))

        # State of Charge
        left_box.add_widget(
            Label(text="STATE OF CHARGE", font_size='20sp', color=(0, 0.75, 1, 1), halign='left', size_hint_y=None,
                  height=50))

        # Progress Bar for state of charge (75%)
        soc_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=50)
        progress_bar = ProgressBar(value=75, max=100)
        soc_box.add_widget(progress_bar)
        soc_box.add_widget(
            Label(text="75%", font_size='18sp', color=(0, 0, 0, 1), size_hint=(None, None), size=(60, 50)))
        left_box.add_widget(soc_box)

        # Battery Power
        left_box.add_widget(
            Label(text="BATTERY POWER", font_size='20sp', color=(0, 0.75, 1, 1), halign='left', size_hint_y=None,
                  height=50))
        left_box.add_widget(
            Label(text="0.00 kW", font_size='40sp', color=(1, 1, 1, 1), halign='left', size_hint_y=None, height=100))

        layout.add_widget(left_box)

        # Right side (Lap times, Battery, Cool Loop, and Status)
        right_box = BoxLayout(orientation='vertical', padding=20, spacing=20)

        # Lap times title
        right_box.add_widget(
            Label(text="Lap", font_size='20sp', color=(0, 0.75, 1, 1), halign='left', size_hint_y=None, height=50))

        # Lap times grid
        laps_grid = GridLayout(cols=2, size_hint_y=None, row_force_default=True, row_default_height=40)

        # Add lap times data
        laps_grid.add_widget(Label(text="1", font_size='20sp', color=(1, 1, 1, 1)))
        laps_grid.add_widget(Label(text="01:28:04", font_size='20sp', color=(1, 1, 1, 1)))
        laps_grid.add_widget(Label(text="2", font_size='20sp', color=(1, 1, 1, 1)))
        laps_grid.add_widget(Label(text="00:44:67", font_size='20sp', color=(1, 1, 1, 1)))
        laps_grid.add_widget(Label(text="3", font_size='20sp', color=(1, 1, 1, 1)))
        laps_grid.add_widget(Label(text="01:33:70", font_size='20sp', color=(1, 1, 1, 1)))
        laps_grid.add_widget(Label(text="4", font_size='20sp', color=(0.75, 0.5, 1, 1)))  # Purple color for active lap
        laps_grid.add_widget(Label(text="00:11:23", font_size='20sp', color=(0.75, 0.5, 1, 1)))
        laps_grid.add_widget(
            Label(text="5", font_size='20sp', color=(0.25, 1, 0.25, 1)))  # Green color for completed lap
        laps_grid.add_widget(Label(text="00:42:00", font_size='20sp', color=(0.25, 1, 0.25, 1)))

        right_box.add_widget(laps_grid)

        # Battery and Cool Loop data at the bottom
        temp_box = GridLayout(cols=2, size_hint_y=None, row_force_default=True, row_default_height=40)
        temp_box.add_widget(Label(text="BATTERY", font_size='18sp', color=(0, 0.75, 1, 1)))
        temp_box.add_widget(Label(text="00 C", font_size='18sp', color=(1, 1, 1, 1)))
        temp_box.add_widget(Label(text="COOL LOOP", font_size='18sp', color=(0, 0.75, 1, 1)))
        temp_box.add_widget(Label(text="22 C", font_size='18sp', color=(1, 1, 1, 1)))
        right_box.add_widget(temp_box)

        layout.add_widget(right_box)

        # VCU status bar at the bottom
        status_bar = Label(text="VCU: Connection lost", font_size='20sp', color=(1, 1, 1, 1), size_hint_y=None,
                           height=50, halign='center')
        status_bar_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=40, padding=[10, 0, 10, 0])
        status_bar_box.add_widget(status_bar)
        status_bar_box.canvas.before.clear()
        status_bar_box.canvas.before.add(Color(1, 0, 0, 1))  # Red background
        status_bar_box.canvas.before.add(Rectangle(pos=status_bar_box.pos, size=status_bar_box.size))

        self.add_widget(layout)
        self.add_widget(status_bar_box)


class MyApp(App):
    def build(self):
        sm = ScreenManager()

        # Adding the overview screen to screen manager
        sm.add_widget(OverviewScreen(name='overview'))

        return sm


if __name__ == '__main__':
    MyApp().run()
