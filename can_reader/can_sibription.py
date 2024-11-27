from dataclasses import dataclass
import canparser
import can
from typing import Callable, TypeVar, Any


# använda pypy för snabbare

T = TypeVar("T", bound=canparser.BaseData)


@dataclass(slots=True)
class HubMessage:
    can_message: can.Message
    parsed_data: T


type_listeners = {}


def subscribe_can_message(message_type: type, callback):
    """
    Subscribe to a CAN message.
    """
    if message_type in type_listeners:
        type_listeners[message_type].append(callback)
    else:
        type_listeners[message_type] = []
        type_listeners[message_type].append(callback)


def publish_message(can_message: can.Message):
    """
    Publish a message to all listeners.
    """
    parsed = canparser.parse_message(can_message)

    hub_message = HubMessage(can_message, parsed)

    # Call all listeners that are listening for this specific type of message
    if type(parsed) in type_listeners:
        for callback in type_listeners[type(parsed)]:
            callback(hub_message)


if __name__ == '__main__':

    temp = 0

    def print_message(message):
        temp = message.parsed_data.temperature_c

    subscribe_can_message(canparser.MotorTemperatureData, print_message)

    publish_message(can.Message(arbitration_id=0x181, data=[0x49, 0x13, 0x25, 0x00]))





# from dataclasses import dataclass
# import canparser
# import can
# from typing import Callable, TypeVar, Any
#
#
# T = TypeVar("T", bound=canparser.BaseData)
#
#
# @dataclass(slots=True)
# class HubMessage:
#     can_message: can.Message
#     parsed_data: T
#
#
# general_listeners: list[Callable[[HubMessage], Any]] = []
# type_listeners: dict[type[T], list[Callable[[HubMessage], Any]]] = {}
#
#
# def listen_for_messages(callback: Callable[[HubMessage], Any]) -> None:
#     """
#     Register a callback to be called when a new message is received.
#
#     :param callback: Called when a new message is received.
#     """
#     general_listeners.append(callback)
#
#
# def listen_for_messages_of_type(message_type: type[T], callback: Callable[[HubMessage], Any]) -> None:
#     """
#     Register a callback to be called when a new message of the given type is received.
#
#     :param message_type: The type of message to listen for.
#     :param callback: Called when a message of the given type is received.
#     """
#     # Add the message type to the dictionary if it is not already there
#     if message_type not in type_listeners:
#         type_listeners[message_type] = []
#
#     type_listeners[message_type].append(callback)
#
#
# def publish_message(can_message: can.Message) -> None:
#     """
#     Publish a message to all listeners.
#     """
#     parsed = canparser.parse_message(can_message)
#
#     hub_message = HubMessage(can_message, parsed)
#
#     # Call all general listeners
#     for callback in general_listeners:
#         callback(hub_message)
#
#     # Call all listeners that are listening for this specific type of message
#     if type(parsed) in type_listeners:
#         for callback in type_listeners[type(parsed)]:
#             callback(hub_message)
