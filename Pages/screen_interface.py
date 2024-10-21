

class ScreenInterface:
    def __init__(self, name):
        self.name = name
        self.screen_switcher = None

    def add_screen_switcher(self, func):
        """
        This func is called to add the screen switcher.
        :param func: is the function from the class CustomScreenSwitcher
        :return: None
        """
        self.screen_switcher = func
        pass

    def update_screen(self, data):
        """
        This func is called to update the screen switcher.
        :param data: The can data.
        :return:
        """
        pass