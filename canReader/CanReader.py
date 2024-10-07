from can import Message
import can
import random
import time
import canparser


class CanBusReader:
    def __init__(self, channel='vcan0', bustype='socketcan'):
        """
        Initialize the CAN bus for real hardware.
        - `channel`: Interface channel (e.g., 'vcan0', 'can0', or 'PCAN_USBBUS1').
        - `bustype`: The type of CAN interface (e.g., 'socketcan', 'pcan', 'kvaser').
        """
        self.bus = can.interface.Bus(channel=channel, bustype=bustype)

    # later
    # def send_message(self, message: CanMessage):
    #     """Send a CAN message on the real CAN bus."""
    #     try:
    #         msg = can.Message(arbitration_id=message.message_id, data=message.data, dlc=message.dlc)
    #         self.bus.send(msg)
    #         print(f"Message sent: {msg}")
    #     except can.CanError as e:
    #         print(f"Error sending message on CAN bus: {e}")

    def read_message(self):
        """
        Reads a single CAN message from the real CAN bus.
        Returns the parsed message class.
        """
        try:
            message = self.bus.recv(timeout=1.0)  # Wait up to 1 second for a message
            if message is None:
                print("No message received within timeout.")
                return None
            print(f"Message received: ID={message.arbitration_id}, Data={message.data}")
            return canparser.parse_message(message)
        except can.CanError as e:
            print(f"Error reading message from CAN bus: {e}")
            return None

    def start_listening(self):
        """ Continuously listen to messages on the real CAN bus. """
        print("Listening to CAN bus...")
        try:
            while True:
                self.read_message()
                time.sleep(0.5)  # Small delay to simulate processing time
        except KeyboardInterrupt:
            print("Stopped listening to CAN bus.")


class CanBusSimulator:
    def __init__(self, channel='vcan0', bustype='socketcan'):
        """
        Initialize the CAN bus simulator without any hardware.
        Simulated messages are stored in a queue (list).
        """
        self.simulated_messages = []

        self.inject_test_messages()

        print("Testing mode enabled. Simulating CAN bus...")

    # def send_message(self, message: CanMessage):
    #     """Simulate sending a CAN message by storing it in the simulated message queue."""
    #     print(f"Simulating message send: {message}")
    #     self.simulated_messages.append(message)

    def read_message(self):
        """
        Simulate receiving a CAN message from the simulated message queue.
        Returns the message if received, or None if no message is available.
        """
        if self.simulated_messages:
            value = self.simulated_messages.pop(0)
            print(f"Simulating message receive: {value}")
            return SpeedData #ändrade till value istället för 0 för annars blev det bara 0 helatiden.
        else:
            print("No simulated messages to receive.")
            return None

    def inject_test_messages(self, count=5):
        """Inject a set of random test messages into the simulated CAN bus."""
        for speed in range(1, 1000):
            message = self.generate_random_test_message(random.randint(200, 350))
            print(f"Injecting simulated message: {message}")
            self.simulated_messages.append(message)

    def generate_random_test_message(self, data):
        """Generate a random CAN message for testing purposes."""
        message_id = 0x7FF
        dlc = random.randint(1, 8)
        return CanMessage(message_id=message_id, data=data, dlc=dlc)

    def start_listening(self):
        """ Continuously listen to messages on the simulated CAN bus. """
        print("Simulated listening to CAN bus...")
        try:
            while True:
                self.read_message()
                time.sleep(0.5)  # Simulating processing delay
        except KeyboardInterrupt:
            print("Stopped listening to simulated CAN bus.")


class CanMessage:
    def __init__(self, message_id: int, data: bytes, dlc: int):
        if not (0 <= message_id <= 0x7FF):
            raise ValueError("Message ID must be in the range 0-2047 (11-bit identifier).")
        self.message_id = message_id
        self.data = data
        self.dlc = dlc

    def __repr__(self):
        return f"CanMessage(ID={self.message_id}, DLC={self.dlc}, Data={self.data})"


class SpeedData:
    def __init__(self, speed: int):
        self.speed = speed