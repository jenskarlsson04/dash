import canparser
from can_reader import subscribe_can_message
import time
from kivy.clock import Clock  # Prototype: For CAN data timeout checking

from can_simulator_er25.src.generators.inverter import inverter_errors


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

        self.faults = set()



        #Set default values
        self.tscu_state = "N/A"
        self.tscu_mode = "N/A"
        self.tscu_errors = ["N/A"]
        self.inv_errors = ["N/A errors"]
        self.inv_warnings = ["N/A warn"]
        self.airplus_state = "N/A"
        self.airminus_state = "N/A"
        self.inv95p = "N/A"
        self.pre = "N/A"
        self.sdc = "N/A"
        self.tsact = "N/A"
        self.error = "N/A"
        self.lvvoltage = "N/A"
        self.orioncurrent = "N/A"
        self.orionvoltage = "N/A"
        self.orionsoc = "N/A"
        self.packtemp_min = "N/A"
        self.packtemp_max = "N/A"
        self.speed = 0
        self.lvvoltage_low = True
        self.vcu_mode = "N/A"





        # -----------------------------
        # Prototype: CAN error tracking (debug/prototype)
        # -----------------------------
        # Define a configuration for each expected channel: threshold (seconds) and fault messages.
        self.channels_config = {
            "oriontemp":     {"threshold": 4, "faults": ["High pack temp", ".High pack temp"]},
            "motortemp":     {"threshold": 4, "faults": ["High motor temp", ".High motor temp"]},
            "inverter_error": {"threshold": 4, "faults": ["Inverter has error"]},
            "inverter_temp": {"threshold": 4, "faults": ["High inverter temp", ".High inverter temp"]},
            "brake_press":   {"threshold": 4, "faults": ["Low Brake pressure", ".Low Brake pressure"]},
            #"cooling_temp":  {"threshold": 4, "faults": ["High cooling temp", ".High cooling temp"]},
            "analogfront":   {"threshold": 4, "faults": ["LV Bat LOW Voltage", ".LV Bat LOW Voltage"]},
            "tscu":    {"threshold": 4, "faults": ["TSCU has error", ".TSCU has error"]},
            "orionpower":    {"threshold": 4, "faults": ["PACK LOW Voltage", ".PACK LOW Voltage",
                                                         "LOW SOC", ".LOW SOC"]},
            "vcu":      {"threshold": 4, "faults" : []},

        }

        # Pre-populate last_update for all channels with the current time
        self.last_update = {}
        current = time.time()
        for channel in self.channels_config:
            self.last_update[channel] = current
            # Create a boolean flag for each channel (e.g. self.oriontemp_fault)
            setattr(self, f"{channel}_fault", False)

        self.can_error = False
        self.can_connected = True
        # Check every 1 second
        Clock.schedule_interval(self.check_can_data, 1)

        # Subscribe to CAN messages
        subscribe_can_message(canparser.OrionTempData, self.oriontemp)
        subscribe_can_message(canparser.MotorTemperatureData, self.motortemp)
        subscribe_can_message(canparser.InverterErrorsData, self.inverter_error)
        subscribe_can_message(canparser.InverterTemperatureData, self.inverter_temp)
        subscribe_can_message(canparser.BrakePressureData, self.brake_press)
        #subscribe_can_message(canparser.CoolingLoopTemperatureData, self.cooling_temp)
        subscribe_can_message(canparser.AnalogCanConverterSensorReadingsDataF, self.analogfront)
        subscribe_can_message(canparser.TscuData, self.tscu)
        subscribe_can_message(canparser.OrionPowerData, self.orionpower)
        subscribe_can_message(canparser.BrakePressureData, self.brake_press)
#        subscribe_can_message(canparser.VcuStateData, self.vcu)
        # add orion power data

    def check_can_data(self, dt):
        """
        For each expected CAN channel, if no message has been received within its threshold,
        remove its non-timeout fault messages and add a timeout fault. Also update a dedicated
        boolean (<channel>_fault) for each channel. Finally, set can_connected to True if all channels
        are healthy.
        """
        current_time = time.time()
        error_found = False

        for channel, config in self.channels_config.items():
            threshold = config["threshold"]
            fault_messages = config["faults"]
            if current_time - self.last_update[channel] > threshold:
                error_found = True
                # Remove any non-timeout faults for this channel.
                for fault in fault_messages:
                    self.faults.discard(fault)
                # Add a timeout fault.
                self.faults.add(f"CAN TIMEOUT: {channel}")
                setattr(self, f"{channel}_fault", True)
            else:
                self.faults.discard(f"CAN TIMEOUT: {channel}")
                setattr(self, f"{channel}_fault", False)

        self.can_error = error_found
        self.can_connected = not error_found

    def oriontemp(self, message):
        self.last_update["oriontemp"] = time.time()
        self.packtemp_max = message.parsed_data.pack_max_cell_temp_c
        self.packtemp_min = message.parsed_data.pack_min_cell_temp_c
        if self.packtemp_max > 60:
            self.faults.add("High pack temp")
            self.faults.discard(".High pack temp")
        elif self.packtemp_max > 50:
            self.faults.add(".High pack temp")
            self.faults.discard("High pack temp")
        else:
            self.faults.discard("High pack temp")
            self.faults.discard(".High pack temp")

    def motortemp(self, message):
        self.last_update["motortemp"] = time.time()
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
        self.last_update["inverter_error"] = time.time()
        if message.parsed_data.decoded_errors:
            self.inv_errors = [error.type for error in message.parsed_data.decoded_errors]
        if message.parsed_data.decoded_warnings:
            self.inv_warnings = [
                warning.type for warning in message.parsed_data.decoded_warnings
            ]
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
        self.last_update["inverter_temp"] = time.time()
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
        self.last_update["brake_press"] = time.time()
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
        self.last_update["cooling_temp"] = time.time()
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
        self.last_update["analogfront"] = time.time()
        self.speed = round((3.6 * 0.2032)*((message.parsed_data.wheel_speed_l_rad_per_sec+message.parsed_data.wheel_speed_r_rad_per_sec)/2))
        if self.analogfront_fault:
            self.lvvoltage = "N/A"
            self.speed = 0
        else:
            self.lvvoltage = round(message.parsed_data.voltage_volts,1)

        if self.lvvoltage < 9.5:
            self.faults.add("LV Bat LOW Voltage")
            self.faults.discard(".LV Bat LOW Voltage")
            self.lvvoltage_low = True
        elif self.lvvoltage < 11.5:
            self.faults.add(".LV Bat LOW Voltage")
            self.faults.discard("LV Bat LOW Voltage")
            self.lvvoltage_low = False
        else:
            self.lvvoltage_low = False
            self.faults.discard("LV Bat LOW Voltage")
            self.faults.discard(".LV Bat LOW Voltage")

    def tscu(self, message):
        self.last_update["tscu"] = time.time()
        if self.tscu_fault:
            self.tscu_state = "N/A"
            self.tscu_mode= "N/A"
            self.airplus_state = "N/A"
            self.airminus_state = "N/A"
            self.inv95p = "N/A"
            self.pre = "N/A"
            self.sdc = "N/A"
            self.tsact = "N/A"
            self.tscu_errors = ["N/A"]
        else:
            self.tscu_state = message.parsed_data.state.name
            self.tscu_mode = message.parsed_data.mode.name
            self.inv95p = message.parsed_data.state_inv95_p
            self.tscu_error_bol = message.parsed_data.has_error
            if message.parsed_data.state_sdc:
                self.sdc = "CLOSED"
            else:
                self.sdc = "OPEN"
            self.tsact = message.parsed_data.state_tsact
            self.pre = message.parsed_data.state_r_pre
            if message.parsed_data.decoded_errors:
                self.tscu_errors = [error.type for error in message.parsed_data.decoded_errors]
            if message.parsed_data.state_r_air_p:
                self.airplus_state = "OPEN"
            else: self.airplus_state = "CLOSED"
            if message.parsed_data.state_r_air_m:
                self.airminus_state = "OPEN"
            else: self.airminus_state = "CLOSED"
        if self.tscu_error_bol:
            self.faults.add("TSCU has error")
        else:
            self.faults.discard("TSCU has error")




    def orionpower(self, message):
        self.last_update["orionpower"] = time.time()
        self.orionsoc = round(100*message.parsed_data.pack_soc_ratio)
        self.orioncurrent = round(message.parsed_data.pack_current_A)
        self.orionvoltage = round(message.parsed_data.pack_voltage_v)

        # Checks
        if self.orionsoc < 0.12:
            self.faults.add("LOW SOC")
            self.faults.discard(".LOW SOC")
        elif self.orionsoc < 0.3:
            self.faults.add(".LOW SOC")
            self.faults.discard("LOW SOC")
        else:
            self.faults.discard("LOW SOC")
            self.faults.discard(".LOW SOC")

        if self.orionvoltage < 330:
            self.faults.add("PACK LOW Voltage")
            self.faults.discard(".PACK LOW Voltage")
        elif self.orionvoltage < 350:
            self.faults.add(".PACK LOW Voltage")
            self.faults.discard("PACK LOW Voltage")
        else:
            self.faults.discard("PACK LOW Voltage")
            self.faults.discard(".PACK LOW Voltage")


    #def vcu(self, message):
     #   self.last_update["vcu"] = time.time()
     #   self.vcu_mode = message.parsed_data.state.name

if __name__ == "__main__":
    from can_reader.simulated_can_class import SimulatedCanClass

    simulated_can_class = SimulatedCanClass()
    simulated_can_class.run()

    shared_data_driver = SharedDataDriver()
    while True:
        pass
