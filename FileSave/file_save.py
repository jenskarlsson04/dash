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
    def __init__(
        self,
        filepath_from_root_folder: str,
        save_interval: float = 0.1,
        data: dict = None,
    ):
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
            with open(temp_path, "wb") as f:
                f.write(orjson.dumps(self.data))

            os.replace(temp_path, self.filepath)  # Atomic file update

    def load(self) -> dict:
        """Loads the dictionary from a file."""
        if not os.path.exists(self.filepath):
            return {}
        with open(self.filepath, "rb") as f:
            self.data = orjson.loads(f.read())

        return self.data

    def reset_file(self):
        self.save(self.data_struct)


if __name__ == "__main__":
    save_to_file = SaveToFile("save.json", data={"key": "value"})
    saver_to_file = SaveToFile("save.json")

    if save_to_file is saver_to_file:
        print("works")
