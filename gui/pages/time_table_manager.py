import random


class TimeTableManager:
    def __init__(self, total_laps=None):
        self.soc = 100  # Initial State of Charge (SOC) in percentage
        self.last_soc = self.soc  # Track SOC before each lap
        self.lap_times = []  # List to store lap times
        self.energy_data = []  # List to store SOC used per lap
        self.all_time_best_lap = None  # Store the all-time best lap time
        self.total_laps = total_laps  # Total laps for the race
        self.completed_laps = 0  # Counter for completed laps

    def add_lap_time(self, lap_time):
        """
        Adds a new lap time and SOC used data.
        Deducts SOC based on random usage and calculates if it is sufficient for remaining laps.
        """
        # Simulate SOC usage for the lap (random deduction between 1-5%)
        new_soc = max(self.soc - random.randint(1, 10), 0)
        soc_used = self.last_soc - new_soc

        # Update SOC tracking
        self.last_soc = new_soc
        self.soc = new_soc

        # Add the lap time and SOC used data
        self.lap_times.append(lap_time)
        self.energy_data.append(soc_used)
        self.completed_laps += 1

        # Keep only the last 2 laps for the dashboard display
        if len(self.lap_times) > 2:
            self.lap_times.pop(0)
            self.energy_data.pop(0)

        # Update all-time best lap
        if self.all_time_best_lap is None or lap_time < self.all_time_best_lap:
            self.all_time_best_lap = lap_time

        # Check if SOC is sufficient for remaining laps
        laps_remaining = self.total_laps - self.completed_laps
        avg_energy_per_lap = (
            sum(self.energy_data) / len(self.energy_data) if self.energy_data else 0
        )
        required_soc = (
            avg_energy_per_lap * laps_remaining
        )  # Delat på 2 pga 11 var endurence sen bryta ström.
        # print(required_soc)
        # print(new_soc)
        # Return whether the remaining SOC is sufficient
        return {
            "best_lap_time": min(self.lap_times),
            "all_time_best_lap": self.all_time_best_lap,
            "lap_times": self.lap_times,
            "energy_data": self.energy_data,
            "soc": self.soc,
            "laps_remaining": laps_remaining,
            "sufficient_soc": self.soc >= required_soc,
            "required_soc": required_soc,
        }

    def compare_last_lap(self, new_lap_time):
        """
        Compares the current lap time with the previous lap.
        Returns 'green' if faster than the previous lap, 'yellow' otherwise.
        """
        if len(self.lap_times) > 1 and new_lap_time < self.lap_times[-2]:
            return "green"
        else:
            return "yellow"

    def format_time(self, time_in_ms):
        """
        Helper function to format the time from milliseconds into mm:ss:ms.
        """
        minutes = time_in_ms // 60000
        seconds = (time_in_ms % 60000) // 1000
        milliseconds = time_in_ms % 1000
        return f"{minutes:02}:{seconds:02}:{milliseconds:03}"
