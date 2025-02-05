from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout


class Orion(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Main layout (vertical BoxLayout)
        main_layout = BoxLayout(orientation='vertical', padding=20, spacing=20)

        # Header layout
        header_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.1), spacing=10)
        header_layout.add_widget(Label(
            text='ORION',
            font_size='70sp',
            color=(0, 1, 1, 1),
            halign='center',
            valign='middle',
            text_size=(None, None)
        ))
        header_layout.add_widget(Label(
            text='DEBUG',
            font_size='70sp',
            color=(0, 1, 1, 1),
            halign='center',
            valign='middle',
            text_size=(None, None)
        ))

        # Left layout (vertical BoxLayout for PACK data)
        left_layout = BoxLayout(orientation='vertical', size_hint=(1, 0.9), spacing=10)

        left_layout.add_widget(Label(
            text='PACK SOC',
            font_size='70sp',
            color=(0, 1, 1, 1),
            size_hint_x=1,
            halign='left',
            valign='middle',
            text_size=(800, None)  # Set width to ensure alignment
        ))

        # SOC layout (horizontal BoxLayout for SOC and %)
        soc_layout = BoxLayout(orientation='horizontal', size_hint=(1, None), height=100, spacing=10)
        soc_layout.add_widget(Label(
            text='000',
            font_size='70sp',
            color=(0, 1, 1, 1),
            halign='right',
            valign='middle',
            text_size=(None, None)
        ))
        soc_layout.add_widget(Label(
            text='%',
            font_size='70sp',
            color=(0, 1, 1, 1),
            halign='left',
            valign='middle',
            text_size=(None, None)
        ))

        left_layout.add_widget(soc_layout)

        left_layout.add_widget(Label(
            text='PACK VOLT',
            font_size='70sp',
            color=(0, 1, 1, 1),
            size_hint_x=1,
            halign='left',
            valign='middle',
            text_size=(800, None)
        ))

        left_layout.add_widget(Label(
            text='PACK CURRENT',
            font_size='70sp',
            color=(0, 1, 1, 1),
            size_hint_x=1,
            halign='left',
            valign='middle',
            text_size=(800, None)
        ))

        # Add layouts to the main layout
        main_layout.add_widget(header_layout)
        main_layout.add_widget(left_layout)

        # Add the main layout to the screen
        self.add_widget(main_layout)

    def refresh(self):
        print()


class OrionDebug(App):
    def build(self):
        return Orion()


if __name__ == '__main__':
    OrionDebug().run()
