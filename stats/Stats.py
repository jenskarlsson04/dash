import json
import time
import os
import threading
from gui.shared_data import SharedDataDriver

# Filvägar i mappen "data"
DATA_DIR = "data"
STATS_FILENAME = os.path.join(DATA_DIR, "stats.json")
PERSISTENT_FILENAME = os.path.join(DATA_DIR, "persistent_stats.json")

# Säkerställ att mappen "data" finns
os.makedirs(DATA_DIR, exist_ok=True)


class Stats:
    def __init__(self):
        self.SharedData = SharedDataDriver()

        default_stats = {
            "orion_current_max": 0,
            "speed_max": 0,
            "pack_temp_max": 0,
            "lv_bat_voltage_min": None,
            "pack_voltage_min": None,
            "power_max": 0,
            "total_run_time": 0,
            "driving_time": 0,
            "consumed_soc": 0,
            "energy_drawn_kwh": 0,
            "distance_driven_m": 0,
            "extra_value_1": "NOT USED",
            "extra_value_2": "NOT USED",
        }

        loaded_stats = self.load_stats()
        if loaded_stats is not None:
            for key, value in default_stats.items():
                if key not in loaded_stats:
                    loaded_stats[key] = value
            self.stats = loaded_stats
            self.start_time = time.time() - self.stats.get("total_run_time", 0)
        else:
            self.stats = default_stats
            self.start_time = time.time()

        self.persistent_stats = self.load_persistent_stats()
        if self.persistent_stats is None:
            self.persistent_stats = {"total_driving_time_s": 0, "distance_driven_km": 0}

        self.initial_soc = None
        self.last_driving_time = time.time()
        self.last_energy_time = time.time()

        # Variabel för att styra bakgrundstråden
        self.running = False

    def refresh(self):
        current_time = time.time()
        self.stats["total_run_time"] = int(current_time - self.start_time)

        try:
            current = float(self.SharedData.orioncurrent)
        except (ValueError, TypeError):
            current = 0
        if current > self.stats["orion_current_max"]:
            self.stats["orion_current_max"] = current

        try:
            speed = float(self.SharedData.speed)
        except (ValueError, TypeError):
            speed = 0
        if speed > self.stats["speed_max"]:
            self.stats["speed_max"] = speed

        try:
            pack_temp = float(self.SharedData.packtemp_max)
        except (ValueError, TypeError):
            pack_temp = 0
        if pack_temp > self.stats["pack_temp_max"]:
            self.stats["pack_temp_max"] = pack_temp

        try:
            lvvolt = float(self.SharedData.lvvoltage)
        except (ValueError, TypeError):
            lvvolt = float("inf")
        if lvvolt < self.stats["lv_bat_voltage_min"]:
            self.stats["lv_bat_voltage_min"] = lvvolt

        try:
            pack_volt = float(self.SharedData.orionvoltage)
        except (ValueError, TypeError):
            pack_volt = float("inf")
        if pack_volt < self.stats["pack_voltage_min"]:
            self.stats["pack_voltage_min"] = pack_volt

        try:
            voltage = float(self.SharedData.orionvoltage)
            current_val = float(self.SharedData.orioncurrent)
            power = (voltage * current_val) / 1000
        except (ValueError, TypeError):
            power = 0
        if power > self.stats["power_max"]:
            self.stats["power_max"] = power

        try:
            soc = float(self.SharedData.orionsoc)
        except (ValueError, TypeError):
            soc = 0
        if self.initial_soc is None:
            self.initial_soc = soc
        consumed = self.initial_soc - soc
        self.stats["consumed_soc"] = consumed if consumed > 0 else 0

        self.update_driving_time()
        self.update_energy()

        self.save_stats()
        self.save_persistent_stats()

    def update_driving_time(self):
        current_time = time.time()
        dt = current_time - self.last_driving_time
        self.last_driving_time = current_time
        try:
            speed = float(self.SharedData.speed)
        except (ValueError, TypeError):
            speed = 0
        if speed > 5:
            self.stats["driving_time"] += dt
            distance = speed * (dt / 3600)
            self.stats["distance_driven_m"] += distance * 1000

            self.persistent_stats["total_driving_time_s"] += dt
            self.persistent_stats["distance_driven_km"] += distance

    def update_energy(self):
        current_time = time.time()
        dt_energy = current_time - self.last_energy_time
        self.last_energy_time = current_time
        try:
            voltage = float(self.SharedData.orionvoltage)
            current_val = float(self.SharedData.orioncurrent)
            power = (voltage * current_val) / 1000
        except (ValueError, TypeError):
            power = 0
        self.stats["energy_drawn_kwh"] += power * (dt_energy / 3600)

    def reset_stats(self):
        default_stats = {
            "orion_current_max": 0,
            "speed_max": 0,
            "pack_temp_max": 0,
            "lv_bat_voltage_min": float("inf"),
            "pack_voltage_min": float("inf"),
            "power_max": 0,
            "total_run_time": 0,
            "driving_time": 0,
            "consumed_soc": 0,
            "energy_drawn_kwh": 0,
            "distance_driven_m": 0,
            "extra_value_1": "NOT USED",
            "extra_value_2": "NOT USED",
        }
        self.stats = default_stats
        self.initial_soc = None
        self.start_time = time.time()
        self.last_driving_time = self.start_time
        self.last_energy_time = self.start_time
        self.save_stats()

    def get_stats(self):
        return self.stats

    def run(self):
        """Startar en bakgrundstråd som periodiskt uppdaterar statistiken."""
        if not self.running:
            self.running = True
            thread = threading.Thread(target=self._run_loop, daemon=True)
            thread.start()

    def _run_loop(self):
        while self.running:
            self.refresh()
            time.sleep(1)

    def stop(self):
        """Stoppar bakgrundstråden."""
        self.running = False
