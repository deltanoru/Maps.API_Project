from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QIcon, QPixmap

import sys
import requests

from settings import *


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.static_api_params = {
            "l": "map",
            "ll": "59.722324,30.416717",
            "size": "600,600"
        }

        uic.loadUi("../graphics/main_window.ui", self)
        self.setWindowTitle("Maps")
        self.setWindowIcon(QIcon("../graphics/maps.ico"))
        self.set_buttons()
        self.search()
        self.set_map_image()

    def set_map_image(self):
        self.pixmap = QPixmap("../graphics/current_map.png")
        self.pic_label.setPixmap(self.pixmap)

    def set_buttons(self):
        self.schedule_btn.clicked.connect(self.set_schedule)
        self.satellite_btn.clicked.connect(self.set_satellite)
        self.hybrid_btn.clicked.connect(self.set_hybrid)
        self.reset_btn.clicked.connect(self.reset)
        self.search_btn.clicked.connect(self.search)

    def set_schedule(self):
        pass

    def set_satellite(self):
        pass

    def set_hybrid(self):
        pass

    def reset(self):
        pass

    def search(self):
        if self.adress_request.text():
            self.static_api_params["ll"] = self.adress_request.text()
        else:
            self.static_api_params["ll"] = "59.722324,30.416717"
        print('searching...')
        response = requests.get(MAP_API_SERVER, params=self.static_api_params)

        if response:
            print('response!')
            with open("../graphics/current_map.png", "wb") as file:
                file.write(response.content)
        self.set_map_image()


def main():
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
