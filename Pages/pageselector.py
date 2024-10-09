from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager

# Global screen manager reference
screen_manager = None

def set_screen_manager(manager: ScreenManager):
    """Set the global screen manager reference."""
    global screen_manager
    screen_manager = manager

def bind_keyboard():
    """Bind the keyboard events for screen switching."""
    Window.bind(on_key_down=on_key_down)

def on_key_down(window, key, scancode, codepoint, modifiers):
    """Handle keyboard events to switch screens when 'K' is pressed."""
    if codepoint == 'k' and screen_manager:
        next_screen()

def next_screen():
    """Switch to the next screen in the ScreenManager."""
    if not screen_manager:
        return  # Ensure the screen manager is set

    current_index = screen_manager.screen_names.index(screen_manager.current)
    next_index = (current_index + 1) % len(screen_manager.screen_names)
    screen_manager.current = screen_manager.screen_names[next_index]
