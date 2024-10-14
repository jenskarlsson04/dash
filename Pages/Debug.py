from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen

class Debug(Screen):
    def __init__(self, **kwargs):
        super(Debug, self).__init__(**kwargs)
        self.orientation = 'horizontal'
        left_section = BoxLayout(orientation='vertical', size_hint=(0.6, 1))
        self.speed_label = Label(text='Debugscreen: Test Mode', font_size='50sp', bold=True, color=(1, 1, 1, 1))
        left_section.add_widget(self.speed_label)
        self.add_widget(left_section)
    pass
