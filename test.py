import tkinter as tk
from tkinter import Label

class VehicleDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Vehicle Dashboard")
        self.root.geometry("500x400")  # Set the size of the window
        self.root.configure(bg="black")  # Set background to black

        # Define the styling variables
        self.text_color = "cyan"
        self.bold_font = ("Arial", 20, "bold")
        self.small_font = ("Arial", 10)
        self.medium_font = ("Arial", 12)
        self.lap_font = ("Arial", 14)

        # Call methods to build the UI
        self.create_velocity_section()
        self.create_soc_section()
        self.create_power_section()
        self.create_lap_times_section()
        self.create_vcu_status()
        self.create_temp_section()

    def create_velocity_section(self):
        """Create the Velocity section of the dashboard."""
        velocity_label = Label(self.root, text="VELOCITY", font=self.small_font, fg=self.text_color, bg="black")
        velocity_label.grid(row=0, column=0, padx=20, sticky="w")

        velocity_value = Label(self.root, text="000 kph", font=self.bold_font, fg="white", bg="black")
        velocity_value.grid(row=1, column=0, padx=20, sticky="w")

    def create_soc_section(self):
        """Create the State of Charge (SOC) section."""
        soc_label = Label(self.root, text="STATE OF CHARGE", font=self.small_font, fg=self.text_color, bg="black")
        soc_label.grid(row=2, column=0, padx=20, sticky="w")

        soc_value = Label(self.root, text="75%", font=self.bold_font, fg="green", bg="black")
        soc_value.grid(row=3, column=0, padx=20, sticky="w")

    def create_power_section(self):
        """Create the Battery Power section."""
        power_label = Label(self.root, text="BATTERY POWER", font=self.small_font, fg=self.text_color, bg="black")
        power_label.grid(row=4, column=0, padx=20, sticky="w")

        power_value = Label(self.root, text="0.00 kW", font=self.bold_font, fg="white", bg="black")
        power_value.grid(row=5, column=0, padx=20, sticky="w")

    def create_lap_times_section(self):
        """Create the Lap Times section."""
        lap_label = Label(self.root, text="Lap", font=self.small_font, fg=self.text_color, bg="black")
        lap_label.grid(row=0, column=1, padx=20, sticky="w")

        time_label = Label(self.root, text="Time", font=self.small_font, fg=self.text_color, bg="black")
        time_label.grid(row=0, column=2, padx=20, sticky="w")

        laps = [
            ("1", "01:28:04"),
            ("2", "00:44:67"),
            ("3", "01:33:70"),
            ("4", "00:11:23", "purple"),
            ("5", "00:42:00", "green")
        ]

        # Display Lap Times
        for i, lap in enumerate(laps):
            lap_number = Label(self.root, text=lap[0], font=self.lap_font, fg="white", bg="black")
            lap_number.grid(row=i + 1, column=1, padx=10, sticky="w")

            lap_time = Label(self.root, text=lap[1], font=self.lap_font, fg=lap[2] if len(lap) == 3 else "white", bg="black")
            lap_time.grid(row=i + 1, column=2, padx=10, sticky="w")

    def create_vcu_status(self):
        """Create the VCU Status section."""
        vcu_status = Label(self.root, text="VCU: Connected", font=self.medium_font, fg="white", bg="green")
        vcu_status.grid(row=6, column=0, columnspan=3, padx=10, pady=20, sticky="ew")

    def create_temp_section(self):
        """Create the Battery and Coolant Loop temperature section."""
        battery_label = Label(self.root, text="BATTERY", font=self.small_font, fg=self.text_color, bg="black")
        battery_label.grid(row=7, column=1, sticky="w")

        cool_label = Label(self.root, text="COOL LOOP", font=self.small_font, fg=self.text_color, bg="black")
        cool_label.grid(row=7, column=2, sticky="w")

        battery_temp = Label(self.root, text="00 C", font=self.medium_font, fg="white", bg="black")
        battery_temp.grid(row=8, column=1, sticky="w")

        cool_temp = Label(self.root, text="22 C", font=self.medium_font, fg="white", bg="black")
        cool_temp.grid(row=8, column=2, sticky="w")


if __name__ == "__main__":
    root = tk.Tk()
    app = VehicleDashboard(root)
    root.mainloop()
