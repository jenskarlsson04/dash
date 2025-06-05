import os
import threading
import time
import orjson


class SaveToFileMeta(type):
    """Metaclass to ensure one instance per file path."""

    _instances = {}

    def __call__(cls, filepath, *args, **kwargs):
        if filepath not in cls._instances:
            cls._instances[filepath] = super().__call__(filepath, *args, **kwargs)
        return cls._instances[filepath]


class SaveToFile(metaclass=SaveToFileMeta):
    def __init__(self, filepath_from_root_folder: str, save_interval: float = 0.1, data: dict = None,):

        # check if file exists:
        if not os.path.exists(filepath_from_root_folder):
            os.makedirs(os.path.dirname(filepath_from_root_folder), exist_ok=True)


        self.filepath = filepath_from_root_folder
        self.data = {}
        self.lock = threading.Lock()
        self.save_interval = save_interval

        self.hase_changed = False

        self.data_struct = data

        if self.load() == {}:
            self.reset_file()

        self.thread = threading.Thread(target=self._save_loop, daemon=True)
        self.thread.start()

    def save(self, new_data: dict):
        """Updates the dictionary and schedules a save."""
        with self.lock:
            self.data.update(new_data)
            self.hase_changed = True

    def _save_loop(self):
        """Background loop that periodically saves the data."""
        while True:
            time.sleep(self.save_interval)
            if self.hase_changed:
                self._save()
                self.hase_changed = False

    def _save(self):
        """Saves the dictionary to a file atomically."""
        with self.lock:
            temp_path = self.filepath + ".tmp"
            try:
                with open(temp_path, "wb") as f:
                    f.write(orjson.dumps(self.data))
                os.replace(temp_path, self.filepath)  # Atomic file update
            except Exception:
                # On failure, schedule retry
                self.hase_changed = True

    def load(self) -> dict:
        """Loads the dictionary from a file."""
        if not os.path.exists(self.filepath):
            return {}
        try:
            with open(self.filepath, "rb") as f:
                raw = f.read()
            self.data = orjson.loads(raw)
        except orjson.JSONDecodeError:
            # Corrupted file: back up original and reset to default structure
            try:
                # Move corrupted file to a timestamped backup
                backup_path = f"{self.filepath}.corrupted.{int(time.time())}"
                os.replace(self.filepath, backup_path)
            except Exception:
                pass
            self.data = {}
            self.reset_file()
        except Exception:
            # Any other I/O error, leave data empty and schedule a save
            self.data = {}
            self.hase_changed = True
        return self.data

    def reset_file(self):
        self.save(self.data_struct)


if __name__ == "__main__":
    save_to_file = SaveToFile("save.json", data={"key": "value"})
    saver_to_file = SaveToFile("save.json")

    if save_to_file is saver_to_file:
        print("works")
