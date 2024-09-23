import tkinter as tk

# Main application class
class MyApp:
    def __init__(self, root):
        """Initialize the main window and the components."""
        self.root = root
        self.root.title("My Application")
        self.root.geometry("400x300")

        # Call method to create widgets
        self.create_widgets()

    def create_widgets(self):
        """Create and arrange the widgets in the window."""
        # Create a label
        self.label = tk.Label(self.root, text="Welcome to MyApp!", font=("Arial", 16))
        self.label.pack(pady=20)

        # Create a button
        self.button = tk.Button(self.root, text="Click Me", command=self.on_button_click)
        self.button.pack(pady=10)

        # Create an entry field
        self.entry = tk.Entry(self.root)
        self.entry.pack(pady=10)

    def on_button_click(self):
        """Handle the button click event."""
        entered_text = self.entry.get()  # Get text from entry
        self.label.config(text=f"Hello, {entered_text}!")  # Update label text


# Entry point for running the application
if __name__ == "__main__":
    root = tk.Tk()  # Create the root window
    app = MyApp(root)  # Initialize the app with the root window
    root.mainloop()  # Start the main loop
