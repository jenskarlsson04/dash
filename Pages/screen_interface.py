

class ScreenInterface:
    def __init__(self):
        self.name = self.__class__.__name__
        self.screen_switcher = None

    def add_screen_switcher(self, func):
        """
        This func is called to add the screen switcher.
        :param func: is the function from the class CustomScreenSwitcher
        :return: None
        """
        self.screen_switcher = func

    def update_screen(self, data):
        """
        This func is called to update the screen switcher.
        :param data: The can data.
        :return:
        """


if __name__ == '__main__':
    # testing
    screen = ScreenInterface()

    class Parent(ScreenInterface):
        def __init__(self):
            super().__init__()
            print('Parent class is called', self.name)

    parent = Parent()

