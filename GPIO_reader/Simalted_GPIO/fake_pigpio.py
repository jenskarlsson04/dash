import time
import threading

# Define constants (same as real pigpio)
INPUT = 0
OUTPUT = 1
PUD_OFF = 0
PUD_DOWN = 1
PUD_UP = 2
RISING_EDGE = 0
FALLING_EDGE = 1
EITHER_EDGE = 2

class FakePi:
    def __init__(self):
        self.pins = {}  # Stores GPIO states
        self.callbacks = {}  # Stores registered callbacks
        print("[FAKE] Initialized pigpio")

    def set_mode(self, gpio, mode):
        self.pins[gpio] = {"mode": mode, "value": 0, "pull": PUD_OFF}
        print(f"[FAKE] Set GPIO {gpio} to mode {mode}")

    def set_pull_up_down(self, gpio, pud):
        if gpio in self.pins:
            self.pins[gpio]["pull"] = pud
            print(f"[FAKE] Set GPIO {gpio} pull-up/down to {pud}")
        else:
            print(f"[FAKE] Warning: GPIO {gpio} not initialized!")

    def write(self, gpio, value):
        if gpio in self.pins and self.pins[gpio]["mode"] == OUTPUT:
            old_value = self.pins[gpio]["value"]
            self.pins[gpio]["value"] = value
            print(f"[FAKE] Set GPIO {gpio} to {value}")

            # Trigger callbacks if value changed
            if old_value != value:
                edge = RISING_EDGE if value == 1 else FALLING_EDGE
                self._trigger_callbacks(gpio, edge)
        else:
            print(f"[FAKE] Warning: GPIO {gpio} is not an OUTPUT!")

    def read(self, gpio):
        if gpio in self.pins:
            return self.pins[gpio]["value"]
        print(f"[FAKE] Warning: GPIO {gpio} not initialized!")
        return 0

    def callback(self, gpio, edge, func):
        if gpio not in self.callbacks:
            self.callbacks[gpio] = []
        self.callbacks[gpio].append((edge, func))
        print(f"[FAKE] Registered callback on GPIO {gpio} for edge {edge}")

    def gpio_trigger(self, gpio, pulse_length=10, level=1):
        """Simulate a pulse on a GPIO pin, regardless of mode."""
        if gpio in self.pins:
            print(f"[FAKE] Triggering GPIO {gpio} with pulse length {pulse_length} µs")

            old_value = self.pins[gpio]["value"]
            self.pins[gpio]["value"] = level  # Set to HIGH or LOW

            # Trigger callbacks if value changed
            edge = RISING_EDGE if level == 1 else FALLING_EDGE
            self._trigger_callbacks(gpio, edge)

            time.sleep(pulse_length / 1_000_000)  # Convert µs to seconds

            # Restore old value
            self.pins[gpio]["value"] = old_value
            self._trigger_callbacks(gpio, FALLING_EDGE if edge == RISING_EDGE else RISING_EDGE)
        else:
            print(f"[FAKE] Warning: GPIO {gpio} not initialized!")

    def _trigger_callbacks(self, gpio, edge):
        """Simulates edge detection callbacks"""
        if gpio in self.callbacks:
            for cb_edge, func in self.callbacks[gpio]:
                if cb_edge == edge or cb_edge == EITHER_EDGE:
                    func(gpio, self.pins[gpio]["value"], time.time())

    def stop(self):
        """Stops the fake pigpio instance"""
        print("[FAKE] Stopping pigpio")

# Drop-in replacement for pigpio.pi()
def pi():
    return FakePi()
