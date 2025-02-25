import canparser
from can_reader import subscribe_can_message
import time


class SharedDataDriver:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(SharedDataDriver, cls).__new__(cls, *args, **kwargs)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, **kwargs):
        if self._initialized:
            return
        self._initialized = True

        self.warnings = set()
        self.faults = set()

        # CAN subscriptions
        subscribe_can_message(canparser.OrionTempData, self.oriontemp)
        subscribe_can_message(canparser.MotorTemperatureData, self.motortemp)
        subscribe_can_message(canparser.InverterErrorsData, self.inverter_error)
        subscribe_can_message(canparser.InverterTemperatureData, self.inverter_temp)
        subscribe_can_message(canparser.BrakePressureData, self.brake_press)
        subscribe_can_message(canparser.CoolingLoopTemperatureData, self.cooling_temp)
        subscribe_can_message(canparser.AnalogCanConverterSensorReadingsDataF, self.analogfront)

        # Values for faults

        # self.warn_low_lv_volt = 9.5
        # self.fault_low_lv_volt = 5.5

    def oriontemp(self, message):
        self.packtemp = message.parsed_data.pack_max_cell_temp_c
        if self.packtemp > 60:
            # Severe error
            self.faults.add("High pack temp")
            self.faults.discard(".High pack temp")
        elif self.packtemp > 50:
            # Less severe error
            self.faults.add(".High pack temp")
            self.faults.discard("High pack temp")
        else:
            self.faults.discard("High pack temp")
            self.faults.discard(".High pack temp")

    def motortemp(self, message):
        self.motortemp = message.parsed_data.temperature_c
        if self.motortemp > 55:
            self.faults.add("High motor temp")
            self.faults.discard(".High motor temp")
        elif self.motortemp > 50:
            self.faults.add(".High motor temp")
            self.faults.discard("High motor temp")
        else:
            self.faults.discard("High motor temp")
            self.faults.discard(".High motor temp")

    def inverter_error(self, message):
        self.inverter_error = message.parsed_data.has_error
        self.inverter_warning = message.parsed_data.has_warning

        if self.inverter_error:
            self.faults.add("Inverter has error")
        else:
            self.faults.discard("Inverter has error")

        if self.inverter_warning:
            self.faults.add(".Inverter has warn")
        else:
            self.faults.discard(".Inverter has warn")

    def inverter_temp(self, message):
        self.inverter_temp = message.parsed_data.temperature_c
        if self.inverter_temp > 60:
            self.faults.add("High inverter temp")
            self.faults.discard(".High inverter temp")
        elif self.inverter_temp > 50:
            self.faults.add(".High inverter temp")
            self.faults.discard("High inverter temp")
        else:
            self.faults.discard("High inverter temp")
            self.faults.discard(".High inverter temp")

    def brake_press(self, message):
        self.brake_press = message.parsed_data.raw_adc
        if self.brake_press < 1500:
            self.faults.add("Low Brake pressure")
            self.faults.discard(".Low Brake pressure")
        elif self.brake_press < 2000:
            self.faults.add(".Low Brake pressure")
            self.faults.discard("Low Brake pressure")
        else:
            self.faults.discard("Low Brake pressure")
            self.faults.discard(".Low Brake pressure")

    def cooling_temp(self, message):
        self.cooling_temp = message.parsed_data.temperature_c
        if self.cooling_temp > 60:
            self.faults.add("High cooling temp")
            self.faults.discard(".High cooling temp")
        elif self.cooling_temp > 50:
            self.faults.add(".High cooling temp")
            self.faults.discard("High cooling temp")
        else:
            self.faults.discard("High cooling temp")
            self.faults.discard(".High cooling temp")

    def analogfront(self, message):
        self.lvvoltage = message.parsed_data.voltage_volts
        if self.lvvoltage < 9.5:
            self.faults.add("LV Bat LOW Voltage")
            self.faults.discard(".LV Bat LOW Voltage")
        elif self.lvvoltage < 11.5:
            self.faults.add(".LV Bat LOW Voltage")
            self.faults.discard("LV Bat LOW Voltage")
        else:
            self.faults.discard("LV Bat LOW Voltage")
            self.faults.discard(".LV Bat LOW Voltage")


if __name__ == "__main__":
    from can_reader.simulated_can_class import SimulatedCanClass

    simulated_can_class = SimulatedCanClass()
    simulated_can_class.run()

    shared_data_driver = SharedDataDriver()
    while True:
        pass
