import os
from FileSave.file_save import SaveToFile

DATA_DIR = "data"

STATS_FILENAME = os.path.join(DATA_DIR, "stats.json")
PERSISTENT_FILENAME = os.path.join(DATA_DIR, "persistent_stats.json")

save_file_data_struct = {
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

SaveToFile(STATS_FILENAME, data=save_file_data_struct)

presistent_data_struct = {"total_driving_time_s": 0, "distance_driven_m": 0}

SaveToFile(PERSISTENT_FILENAME, data=presistent_data_struct)
