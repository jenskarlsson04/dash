from gui_main import MainApp
from can_reader import CanClass

main_app = MainApp()

can_class = CanClass()
can_class.start_read_can()

import FileSave

stats = FileSave.SaveToFile(FileSave.STATS_FILENAME)

stats.load()




def run():
    main_app.run()


if __name__ == "__main__":
    run()
