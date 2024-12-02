import can
from can_simulator_er25.src.simulation import Simulation
from can_simulator_er25.src.generators.vcu import VCU_generators
from can_simulator_er25.src.generators.orion import Orion_generators
from can_simulator_er25.src.generators.btmu import BTMU_generators
from threading import Thread
from can_reader.can_sibription import publish_message


class SimulatedCanClass:
    def __init__(self):
        self.connected = False

        # Create two linked virtual CAN buses
        self._bus1 = can.Bus("test", interface="virtual")
        self._bus2 = can.Bus("test", interface="virtual")

        generators = [*VCU_generators, *Orion_generators, *BTMU_generators]
        on_new_message = lambda message: self._bus1.send(message)
        simulation_speed = 1.0

        self.can_simulation = Simulation(generators, on_new_message, simulation_speed)

        self.thread = Thread(target=self.__thread_func, daemon=True)

    def __connect(self, bitrate: int):
        self.connected = True
        self.can_simulation.start()

    def __disconnect(self):
        self.connected = False
        self.can_simulation.stop()

    def __send(self, message: can.Message) -> None:
        if not self.connected:
            raise Exception("Can't send message. Not connected to CAN bus")

    def __receive(self) -> can.Message:
        if not self.connected:
            raise Exception("Can't receive message. Not connected to CAN bus")

        return self._bus2.recv()

    def __thread_func(self):

        self.__connect(500_000)

        while self.connected:
            data = self.__receive()
            publish_message(data)

        self.__disconnect()

    def run(self):
        self.thread.start()