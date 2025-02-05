import can
from .can_sibription import publish_message
from threading import Thread


class CanClass:
    def __init__(self):

        self.can = can.interface.Bus(interface='socketcan', channel='can0', bitrate=500000)
        self.can_recv_timeout_sec = 0.01

        self.thread = Thread(target=self.read_can, daemon=True)

    def start_read_can(self):
        self.thread.start()

    def read_can(self):
        while True:
            message = self.can.recv(self.can_recv_timeout_sec)
            publish_message(message)
