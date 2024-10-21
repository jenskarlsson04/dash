class TimeTableManager:
    def __init__(self):
        self.lap_times = []  # List to store lap times (up to 5)
        self.energy_data = []  # List to store SOC used for each lap
        self.all_time_best_lap = None  # Store the all-time best lap time

    def add_lap_time(self, lap_time, soc_used):
        """
        Adds a new lap time and SOC used data, ensuring only the last 5 laps are kept.
        Tracks the all-time best lap and returns the best lap time of the last 5 laps.
        """
        # Add new lap time and SOC used data
        self.lap_times.append(lap_time)
        self.energy_data.append(soc_used)

        # Keep only the last 5 lap times and SOC values
        if len(self.lap_times) > 5:
            self.lap_times.pop(0)
            self.energy_data.pop(0)

        # Update the all-time best lap
        if self.all_time_best_lap is None or lap_time < self.all_time_best_lap:
            self.all_time_best_lap = lap_time

        # Find the best lap time from the last 5 laps
        best_lap_time = min(self.lap_times)

        return best_lap_time, self.all_time_best_lap, self.lap_times, self.energy_data

    def update_lap_display(self, lap_labels, time_labels, energy_labels):
        """
        Updates the lap display labels with the current lap times and SOC used values.
        Highlights the best lap time of the last 5 laps in green.
        """
        # Check if we have lap times to display
        if not self.lap_times:
            return

        # Find the best lap time from the last 5 laps
        best_lap_time = min(self.lap_times)

        # Loop through the laps and update the labels
        for i, (lap_time, soc_used) in enumerate(zip(self.lap_times, self.energy_data)):
            # Update the lap time label
            time_labels[i].text = self.format_time(lap_time)

            # Update the SOC used label
            energy_labels[i].text = f"{soc_used:.2f}%"

            # Highlight the best lap in green, others in white
            if lap_time == best_lap_time:
                time_labels[i].color = (0, 1, 0, 1)  # Green for best lap among last 5
            else:
                time_labels[i].color = (1, 1, 1, 1)  # White for other laps

    def compare_last_lap(self, new_lap_time):
        """
        Compares the current lap time with the previous lap.
        Returns 'green' if faster than the previous lap, 'yellow' otherwise.
        """
        if len(self.lap_times) > 1 and new_lap_time < self.lap_times[-2]:
            return 'green'
        else:
            return 'yellow'

    def format_time(self, time_in_ms):
        """
        Helper function to format the time from milliseconds into mm:ss:ms.
        """
        minutes = time_in_ms // 60000
        seconds = (time_in_ms % 60000) // 1000
        milliseconds = time_in_ms % 1000
        return f"{minutes:02}:{seconds:02}:{milliseconds:03}"
