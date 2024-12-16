from gui_main import MainApp
from can_reader.simulated_can_class import SimulatedCanClass
from kivy.config import Config

main_app = MainApp()

simulated_can_class = SimulatedCanClass()


Config.set('graphics', 'width', '720')        # Width of the device
Config.set('graphics', 'height', '1280')      # Height of the device
Config.set('graphics', 'density', '2')        # Logical density (e.g., HDPI)
Config.set('graphics', 'dpi', '320')          # Dots per inch for the screen

def run():

    simulated_can_class.run()

    main_app.run()


if __name__ == '__main__':
    run()