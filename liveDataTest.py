import tkinter as tk
import time


class LiveDataApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Live Time with Milliseconds")
        self.root.geometry("300x200")

        # Create a label to display live time with milliseconds
        self.label = tk.Label(root, text="Initializing...", font=("Arial", 24))
        self.label.pack(pady=50)

        """Create and arrange the widgets in the window."""
        # Create a label
        self.label2 = tk.Label(self.root, text="Welcome to MyApp!", font=("Arial", 16))
        self.label2.pack(pady=20)

        # Create a button
        self.button = tk.Button(self.root, text="Click Me", command=self.on_button_click)
        self.button.pack(pady=10)

        # Create an entry field
        self.entry = tk.Entry(self.root)
        self.entry.pack(pady=10)

        # Start the live time update loop
        self.update_live_time()

    def on_button_click(self):
        """Handle the button click event."""
        entered_text = self.entry.get()  # Get text from entry
        self.label.config(text=f"Hello, {entered_text}!")  # Update label text

        print("works")

    def update_live_time(self):
        """Display the current time including milliseconds."""

        time.sleep(1)
        # Get current time in seconds since epoch and format with milliseconds
        current_time = time.strftime('%H:%M:%S') + '.' + str(int(time.time() * 1000) % 1000).zfill(3)

        # Update label with the current time and milliseconds
        self.label2.config(text=current_time)

        # Re-run this method after 1 millisecond to update live time
        self.root.after(1, self.update_live_time)


# Running the application
if __name__ == "__main__":
    root = tk.Tk()
    app = LiveDataApp(root)
    root.mainloop()
