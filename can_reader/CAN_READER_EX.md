Yes, it is possible to batch updates in your Kivy application so that the GUI updates only at a set frame rate (e.g., 60 FPS), regardless of how often CAN messages are received. This can be achieved by storing the received CAN messages in a buffer and updating the GUI only at the specified interval.

Here's how you can implement this approach:

1. **Buffer the CAN Messages**: Use a list to store incoming CAN messages.
2. **Update GUI at a Fixed Rate**: In your update function scheduled with Kivy's `Clock`, process the buffered CAN messages and update the GUI accordingly.

### Modified Example Code

Here's how you can adjust the previous example to implement batch updates for CAN messages:

```python
import threading
import time
import can  # Make sure python-can is installed
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from kivy.clock import Clock


class Window1(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.label = Label(text="Waiting for CAN data...")
        self.add_widget(self.label)

    def update_display(self, can_data):
        # Update the label text with the latest CAN data
        self.label.text = f"CAN Data: {can_data}"


class WindowSwitcherApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.can_data_buffer = []  # Buffer for received CAN messages
        self.is_running = True

    def build(self):
        self.sm = ScreenManager()
        self.window1 = Window1(name='window1')
        self.sm.add_widget(self.window1)

        # Schedule the update function at 60 FPS
        Clock.schedule_interval(self.process_can_data, 1/60)

        # Start the CAN reading in a separate thread
        can_thread = threading.Thread(target=self.read_can_data)
        can_thread.daemon = True
        can_thread.start()

        return self.sm

    def read_can_data(self):
        # Initialize the CAN interface (change to your specific configuration)
        bus = can.interface.Bus(channel='can0', bustype='socketcan')

        while self.is_running:
            try:
                message = bus.recv()  # Blocking call to receive CAN message
                if message is not None:
                    # Add received message to the buffer
                    can_message = f"ID: {message.arbitration_id}, Data: {message.data.hex()}"
                    self.can_data_buffer.append(can_message)
            except Exception as e:
                print(f"Error reading CAN data: {e}")

    def process_can_data(self, dt):
        if self.can_data_buffer:
            # Update the GUI with the most recent CAN data
            can_data = self.can_data_buffer[-1]  # Get the latest CAN message
            self.window1.update_display(can_data)
            self.can_data_buffer.clear()  # Clear the buffer after processing

    def on_stop(self):
        self.is_running = False


if __name__ == '__main__':
    WindowSwitcherApp().run()
```

### Explanation of Changes

1. **Buffer for CAN Messages**:
    - A list called `self.can_data_buffer` is used to store incoming CAN messages.

2. **Reading CAN Messages**:
    - In the `read_can_data` method, each received CAN message is formatted and appended to `self.can_data_buffer` without updating the GUI immediately.

3. **Processing CAN Data**:
    - The `process_can_data` method is scheduled to run 60 times per second using `Clock.schedule_interval`. This method checks if there are any messages in the buffer.
    - If there are messages, it retrieves the most recent one, updates the GUI, and then clears the buffer. This ensures the GUI only updates at the desired frame rate.

### Performance Considerations

- **Batch Processing**: By using a buffer, you ensure that all incoming CAN messages are processed at the set frame rate, reducing the overhead of frequent GUI updates.
- **Thread Safety**: In this simple example, accessing `self.can_data_buffer` is safe because it's only updated in one thread (the CAN reading thread) and accessed in another (the GUI update). For more complex scenarios, consider using locks or other synchronization methods.
- **Latency**: This approach may introduce a slight delay in displaying incoming CAN messages (up to one frame if multiple messages are received), but it ensures a smooth GUI experience.

This implementation will allow you to efficiently read CAN data while maintaining a responsive Kivy GUI that updates at 60 FPS.