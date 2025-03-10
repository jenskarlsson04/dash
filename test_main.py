from gui_main import MainApp
from can_reader.simulated_can_class import SimulatedCanClass
from GPIO_reader import set_debug
from stats.Stats import Stats

set_debug()

main_app = MainApp()

simulated_can_class = SimulatedCanClass()
stats = Stats()


def run():

    simulated_can_class.run()
    stats.run()
    main_app.run()


if __name__ == "__main__":
    run()
