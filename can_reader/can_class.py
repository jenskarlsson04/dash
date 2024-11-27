import can
from .can_sibription import publish_message
from threading import Thread
from canparser import MotorTemperatureData


class Can:
    def __init__(self):

        self.can = can.interface.Bus(interface='socketcan', channel='vcan0', bitrate=500000)
        self.can_recv_timeout_sec = 0.01

        self.thread = Thread(target=self.read_can, daemon=True)

    def start_read_can(self):
        self.thread.start()

    def read_can(self):
        while True:
            message = self.can.recv(self.can_recv_timeout_sec)
            publish_message(message)


class CanTest():
    def __init__(self):

        self.thread = Thread(target=self.read_can, daemon=True)

    def start_read_can(self):
        self.thread.start()

    def read_can(self):
        while True:
            message = MotorTemperatureData(22.5)
            publish_message(message)