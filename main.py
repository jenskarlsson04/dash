from kivy.app import App
from pages import Dashboard


# Main App Class
class CarDashboardApp(App):
    def build(self):
        return Dashboard()


if __name__ == '__main__':
    CarDashboardApp().run()