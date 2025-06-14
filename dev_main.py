from gui_main import MainApp
from can_reader.simulated_can_class import SimulatedCanClass

main_app = MainApp()

simulated_can_class = SimulatedCanClass()


def run():

    simulated_can_class.run()
    main_app.run()


if __name__ == "__main__":
    run()
