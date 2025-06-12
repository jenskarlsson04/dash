import canparser
from can_reader import subscribe_can_message
import time
from kivy.clock import Clock  # Prototype: For CAN data timeout checking
from FileSave import SaveToFile, STATS_FILENAME, PERSISTENT_FILENAME


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

        # Vars for saving data to the files
        self.stats_file = SaveToFile(STATS_FILENAME)
        self.pres_stat_file = SaveToFile(PERSISTENT_FILENAME)

        Clock.schedule_interval(self.check_can_data, 1)
        Clock.schedule_interval(self.savefile, 1)
        Clock.schedule_interval(self.calculate_efficiency_score, 1)
        self._initialized = True
        self.faults = set()

        # Set default values (used if can does not connect)
        self.tscu_state = "N/A"
        self.tscu_mode = "N/A"
        self.tscu_errors = ["N/A"]
        self.inv_errors = ["Errors N/A"]
        self.inv_warnings = []
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
        self.inverter_temperature = "N/A"
        self.motor_temperature = "N/A"

        self.stats = self.stats_file.load()
        self.pres_stat = self.pres_stat_file.load()

        # Attributes for low-pass filtering speed
        self.speed_filter_alpha = 0.05  # adjust between 0 and 1; lower is smoother
        self.filtered_speed = 0.0
        self.last_drive_update = time.time()
        self.last_energy_time = time.time()




        # -----------------------------
        # CAN error tracking
        # -----------------------------
        # Define a configuration for each expected channel: threshold (seconds) and fault messages
        # IF YOU WANT TO ADD SOMETHING, YOU NEED TO ADD IT TO channels_config AND channel_to_attr.
        self.channels_config = {
            "oriontemp": {
                "threshold": 2,
                "faults": ["High pack temp", ".High pack temp"],
            },
            "motortemp": {
                "threshold": 2,
                "faults": ["High motor temp", ".High motor temp"],
            },
            "inverter_error": {"threshold": 2, "faults": ["Inverter has error"]},
            "inverter_temp": {
                "threshold": 2,
                "faults": ["High inverter temp", ".High inverter temp"],
            },
            "brake_press": {
                "threshold": 2,
                "faults": ["Low Brake pressure", ".Low Brake pressure"],
            },
            # "cooling_temp": {"threshold": 4, "faults": ["High cooling temp", ".High cooling temp"]},
            "analogfront": {
                "threshold": 2,
                "faults": ["LV Bat LOW Voltage", ".LV Bat LOW Voltage"],
            },
            "tscu": {"threshold": 2, "faults": ["TSCU has error", ".TSCU has error"]},
            "orionpower": {
                "threshold": 2,
                "faults": [
                    "PACK LOW Voltage",
                    ".PACK LOW Voltage",
                    "LOW SOC",
                    ".LOW SOC",
                ],
            },
            "vcu": {"threshold": 2, "faults": []},
        }

        # Pre-populate last_update for all channels with the current time
        self.last_update = {}
        current = time.time()
        for channel in self.channels_config:
            self.last_update[channel] = current

        self.can_error = False
        self.can_connected = True
        self.test_can = False #if True it prints the channel and the delta of recived msg from can



        # Subscribe to CAN messages
        subscribe_can_message(canparser.VcuStateData, self.vcu)
        subscribe_can_message(canparser.OrionTempData, self.oriontemp)
        subscribe_can_message(canparser.MotorTemperatureData, self.motortemp)
        subscribe_can_message(canparser.InverterErrorsData, self.inverter_error)
        subscribe_can_message(canparser.InverterTemperatureData, self.inverter_temp)
        #subscribe_can_message(canparser.BrakePressureData, self.brake_press) unused
        subscribe_can_message(canparser.VcuCoolingAndBrakeData, self.cooling_temp)
        subscribe_can_message(canparser.AnalogCanConverterSensorReadingsDataF, self.analogfront)
        subscribe_can_message(canparser.TscuData, self.tscu)
        subscribe_can_message(canparser.OrionPowerData, self.orionpower)

        # add orion power data


    def update_faults(
        value,
        severe_fault,
        less_servere,
        servere_fault_msg,
        less_servere_msg,
        faults_set,
        inverted=False,
    ):
        """
        Updates the fault set based on the value.
        For non-inverted comparisons (higher value is worse):
          - If value > severe_fault, adds the severe fault message.
          - Else if value > less_servere, adds the less severe fault message.
        For inverted comparisons (lower value is worse):
          - If value < severe_fault, adds the severe fault message.
          - Else if value < less_servere, adds the less severe fault message.
        Otherwise, clears both fault messages.
        """
        # Skip fault handling if value is non-numeric (e.g., "N/A")
        try:
            numeric_value = float(value)
        except (TypeError, ValueError):
            return
        if not inverted:
            if numeric_value > severe_fault:
                faults_set.add(servere_fault_msg)
                faults_set.discard(less_servere_msg)
            elif numeric_value > less_servere:
                faults_set.add(less_servere_msg)
                faults_set.discard(servere_fault_msg)
            else:
                faults_set.discard(servere_fault_msg)
                faults_set.discard(less_servere_msg)
        else:
            if numeric_value < severe_fault:
                faults_set.add(servere_fault_msg)
                faults_set.discard(less_servere_msg)
            elif numeric_value < less_servere:
                faults_set.add(less_servere_msg)
                faults_set.discard(servere_fault_msg)
            else:
                faults_set.discard(servere_fault_msg)
                faults_set.discard(less_servere_msg)

    def check_can_data(self, dt):
        # Map each channel to the list of attributes to update on timeout
        CHANNEL_TO_ATTR = {
            "oriontemp": ["packtemp_max", "packtemp_min"],
            "motortemp": ["motortemp"],
            "inverter_error": ["inv_errors", "inv_warnings", "inverter_warning"],
            "inverter_temp": ["inverter_temp"],
            "brake_press": ["brake_press"],
            "analogfront": ["lvvoltage"], # add speed
            "tscu": [
                "tscu_state",
                "tscu_mode",
                "airplus_state",
                "airminus_state",
                "inv95p",
                "pre",
                "sdc",
                "tsact",
                "tscu_errors",
            ],
            "orionpower": ["orionsoc", "orioncurrent", "orionvoltage"],
            "vcu": ["vcu_mode"],
        }

        self.last_can_update = time.time()
        error_found = False

        for channel, config in self.channels_config.items():
            threshold = config["threshold"]
            if self.last_can_update - self.last_update[channel] > threshold:
                error_found = True
                # Clear previous fault messages for this channel
                for fault in config["faults"]:
                    self.faults.discard(fault)
                #self.faults.add(f"CAN TIMEOUT: {channel}") DISABLED DUE TO CLUTTER

                # Set all associated attributes to "N/A"
                if channel in CHANNEL_TO_ATTR:
                    for attr in CHANNEL_TO_ATTR[channel]:
                        setattr(self, attr, "N/A")

            if self.test_can:
                print(channel, (self.last_can_update-self.last_update[channel]))

            #else:
                #self.faults.discard(f"CAN TIMEOUT: {channel}") DISABLED DUE TO CLUTTER

        self.can_error = error_found
        self.can_connected = not error_found


    def calculate_efficiency_score(self, dt):
        self.vehicle_mass_kg = 240
        self.acc_x_g = 0.4

        force_n = self.acc_x_g * self.vehicle_mass_kg * 9.81
        velocity_m_per_s = self.speed / 3.6
        work_joules = force_n * velocity_m_per_s

        try:
            input_power_w = float(self.orionvoltage) * float(self.orioncurrent)
            score = work_joules / input_power_w if input_power_w > 0 else 0
        except (ValueError, TypeError):
            score = 0

        # Initialize accumulators if missing
        if "effscore_total" not in self.stats:
            self.stats["effscore_total"] = 0.0
        if "effscore_count" not in self.stats:
            self.stats["effscore_count"] = 0

        # Update total and count
        self.stats["effscore_total"] += score
        self.stats["effscore_count"] += 1

        # Compute average
        avg_score = self.stats["effscore_total"] / self.stats["effscore_count"]
        self.stats["effscore"] = max(0.0, min(avg_score, 1.0))



    # Add this new method to the class:
    def update_drive_metrics(self):
        current_time = time.time()
        delta_time = current_time - self.last_drive_update
        self.last_drive_update = current_time
        if self.speed > 5:
            # Add time
            self.stats["driving_time"] = self.stats.get("driving_time", 0) + delta_time
            self.pres_stat["total_driving_time_s"] = self.pres_stat.get("total_driving_time_s", 0) + delta_time

            # Add distance
            distance_m = (self.speed * delta_time) / 3.6  # speed in km/h
            self.stats["distance_driven_m"] = self.stats.get("distance_driven_m", 0) + distance_m
            self.pres_stat["distance_driven_m"] = self.pres_stat.get("distance_driven_m", 0) + distance_m

            # Save updates


    def oriontemp(self, message):
        self.last_update["oriontemp"] = time.time()  # used for can timeout mesurement
        self.packtemp_max = (
            message.parsed_data.pack_max_cell_temp_c
        )  # subscribes on the data from the parser
        self.packtemp_min = (
            message.parsed_data.pack_min_cell_temp_c
        )  # subscribes on the data from the parser

        SharedDataDriver.update_faults(
            self.packtemp_max,
            severe_fault=56,  # Value for when the fault is red and "servere"
            less_servere=50,  # Value for when the fault is yellow and "less servere"
            servere_fault_msg="High pack temp",  # MSG for servere
            less_servere_msg=".High pack temp",  # MSG for less servere
            faults_set=self.faults,
        )
        if self.packtemp_max > self.stats.get("pack_temp_max", 0):
            self.stats["pack_temp_max"] = self.packtemp_max

    def vcu(self, message):
        self.last_update["vcu"] = time.time()
        self.vcu_mode = message.parsed_data.state.name

    def motortemp(self, message):
        self.last_update["motortemp"] = time.time()
        self.motor_temperature = round(message.parsed_data.temperature_c)

        SharedDataDriver.update_faults(
            self.motor_temperature,
            severe_fault=100,
            less_servere=85,
            servere_fault_msg="High motor temp",
            less_servere_msg=".High motor temp",
            faults_set=self.faults,
        )

    def inverter_error(self, message):
        self.last_update["inverter_error"] = time.time()
        if message.parsed_data.decoded_errors:
            self.inv_errors = [
                error.type for error in message.parsed_data.decoded_errors
            ]
        if message.parsed_data.decoded_warnings:
            self.inv_warnings = [
                warning.type for warning in message.parsed_data.decoded_warnings
            ]
        self.inverter_warning = message.parsed_data.has_warning

        # Non-threshold based fault handling
        if message.parsed_data.decoded_errors:
            self.faults.add("Inverter has error")
        else:
            self.faults.discard("Inverter has error")
        if self.inverter_warning:
            self.faults.add(".Inverter has warn")
        else:
            self.faults.discard(".Inverter has warn")

    def inverter_temp(self, message):
        self.last_update["inverter_temp"] = time.time()
        self.inverter_temperature = round(message.parsed_data.temperature_c)

        SharedDataDriver.update_faults(
            self.inverter_temperature,
            severe_fault=83,
            less_servere=72,
            servere_fault_msg="High inverter temp",
            less_servere_msg=".High inverter temp",
            faults_set=self.faults,
        )

    #def brake_press(self, message):
    #    self.last_update["brake_press"] = time.time()
    #    self.brake_press = message.parsed_data.raw_adc
#
    #    SharedDataDriver.update_faults(
    #        self.brake_press,
    #        severe_fault=1500,
    #        less_servere=2000,
    #        servere_fault_msg="Low Brake pressure",
    #        less_servere_msg=".Low Brake pressure",
    #        faults_set=self.faults,
      #      inverted=True,
      #  )

    def cooling_temp(self, message):
        self.last_update["cooling_temp"] = time.time()
        self.cooling_temp = message.parsed_data.cooling_loop_temp_C

        SharedDataDriver.update_faults(
            self.cooling_temp,
            severe_fault=55,
            less_servere=45,
            servere_fault_msg="High cooling temp",
            less_servere_msg=".High cooling temp",
            faults_set=self.faults,
        )

    def analogfront(self, message):
        self.last_update["analogfront"] = time.time()
        # Compute raw speed from wheel speeds
        raw_speed = round(
            (3.6 * 0.2081210191)*message.parsed_data.wheel_speed_r_rad_per_sec)
        # Apply low-pass filter to speed
        self.filtered_speed = (
            self.speed_filter_alpha * raw_speed
            + (1 - self.speed_filter_alpha) * self.filtered_speed
        )
        self.speed = round(self.filtered_speed)
        #self.update_driving_time()
        if self.speed > self.stats.get("speed_max", 0):
            self.stats["speed_max"] = self.speed

        self.lvvoltage = round(message.parsed_data.voltage_volts, 1)

        #Save to stats

        if self.lvvoltage < self.stats.get("lv_bat_voltage_min", 0):
            self.stats["lv_bat_voltage_min"] = self.lvvoltage

        self.update_drive_metrics()

        SharedDataDriver.update_faults(
            self.lvvoltage,
            severe_fault=11.5,
            less_servere=12,
            servere_fault_msg="LV Bat LOW Voltage",
            less_servere_msg=".LV Bat LOW Voltage",
            faults_set=self.faults,
            inverted=True,
        )
        self.lvvoltage_low = self.lvvoltage < 9.5

    def tscu(self, message):
        self.last_update["tscu"] = time.time()
        self.tscu_state = message.parsed_data.state.name
        self.tscu_mode = message.parsed_data.mode.name
        self.inv95p = message.parsed_data.state_inv95_p
        self.tscu_error_bol = message.parsed_data.has_error

        self.sdc = "CLOSED" if message.parsed_data.state_sdc else "OPEN"
        self.tsact = message.parsed_data.state_tsact
        self.pre = message.parsed_data.state_r_pre

        if message.parsed_data.decoded_errors:
            self.tscu_errors = [
                error.type for error in message.parsed_data.decoded_errors
            ]
        else:
            self.tscu_errors = ["N/A"]

        self.airplus_state = "OPEN" if message.parsed_data.state_r_air_p else "CLOSED"
        self.airminus_state = "OPEN" if message.parsed_data.state_r_air_m else "CLOSED"

        if self.tscu_error_bol:
            self.faults.add("TSCU has error")
        else:
            self.faults.discard("TSCU has error")

    def update_consumed_soc(self):
        try:
            soc = int(self.orionsoc)
        except (ValueError, TypeError):
            soc = 0

        # First-time initialization
        if not hasattr(self, "last_soc"):
            self.last_soc = soc

        # If SOC dropped, count the drop as consumption
        delta = self.last_soc - soc
        if delta > 0:
            self.stats["consumed_soc"] = self.stats.get("consumed_soc", 0) + delta

        # Update last seen SOC
        self.last_soc = soc



    def orionpower(self, message):
        self.last_update["orionpower"] = time.time()
        self.orionsoc = round(100 * message.parsed_data.pack_soc_ratio)
        self.orioncurrent = round(message.parsed_data.pack_current_A)
        self.orionvoltage = round(message.parsed_data.pack_voltage_v)

        if self.stats.get("orion_current_max", 0) < self.orioncurrent:
            self.stats["orion_current_max"] = self.orioncurrent


        if self.orionvoltage < self.stats.get("pack_voltage_min", 0):
            self.stats["pack_voltage_min"] = self.orionvoltage

        self.power = round((self.orionvoltage * self.orioncurrent) / 1000)

        if self.power > self.stats.get("power_max", 0):
            self.stats["power_max"] = self.power

        current_time = time.time()
        dt_energy = current_time - self.last_energy_time
        self.last_energy_time = current_time
        try:
            voltage = round(self.orionvoltage)
            current_val = round(self.orioncurrent)
            power = (voltage * current_val)
        except (ValueError, TypeError):
            power = 0
        self.stats["energy_drawn_wh"] = self.stats.get("energy_drawn_wh", 0) + power * (dt_energy / 3600)

        self.update_consumed_soc()

        # Update SOC faults (inverted: lower SOC is worse)
        SharedDataDriver.update_faults(
            self.orionsoc,
            severe_fault=0.05,
            less_servere=0.15,
            servere_fault_msg="LOW SOC",
            less_servere_msg=".LOW SOC",
            faults_set=self.faults,
            inverted=True,
        )

        # Update voltage faults (inverted: lower voltage is worse)
        SharedDataDriver.update_faults(
            self.orionvoltage,
            severe_fault=100, #this value is not intended to be correct
            less_servere=450,
            servere_fault_msg="PACK LOW Voltage",
            less_servere_msg=".PACK LOW Voltage",
            faults_set=self.faults,
            inverted=True,
        )


    def savefile(self, dt):
        self.stats_file.save(self.stats)
        self.pres_stat_file.save(self.pres_stat)

    def reset(self):
        self.stats = {
    "orion_current_max": 0,
    "speed_max": 0,
    "pack_temp_max": 0,
    "lv_bat_voltage_min": 999,
    "pack_voltage_min": 999,
    "power_max": 0,
    "effscore": 0,
    "driving_time": 0,
    "consumed_soc": 0,
    "energy_drawn_wh": 0,
    "distance_driven_m": 0,
    "effscore_total": 0,
    "effscore_count": 0,
}




if __name__ == "__main__":
    from can_reader.simulated_can_class import SimulatedCanClass

    simulated_can_class = SimulatedCanClass()
    simulated_can_class.run()

    shared_data_driver = SharedDataDriver()
    while True:
        pass
