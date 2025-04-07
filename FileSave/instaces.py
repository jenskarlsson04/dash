import os
from FileSave.file_save import SaveToFile

DATA_DIR = "data"

STATS_FILENAME = os.path.join(DATA_DIR, "stats.json")
PERSISTENT_FILENAME = os.path.join(DATA_DIR, "persistent_stats.json")

save_file_data_struct = {
    "orion_current_max": None,
    "speed_max": None,
    "pack_temp_max": None,
    "lv_bat_voltage_min": None,
    "pack_voltage_min": None,
    "power_max": None,
    "total_run_time": None,
    "driving_time": None,
    "consumed_soc": None,
    "energy_drawn_kwh": None,
    "distance_driven_m": None,
    "extra_value_1": None,
    "extra_value_2": None,
}

SaveToFile(STATS_FILENAME, data=save_file_data_struct)

presistent_data_struct = {"total_driving_time_s": None, "distance_driven_km": None}

SaveToFile(PERSISTENT_FILENAME, data=save_file_data_struct)
