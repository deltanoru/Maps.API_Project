from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit
from PyQt5.QtGui import QIcon, QPixmap

import sys
import requests
# connect 2(
from settings import *
from support import get_coords


class MainWindow(QMainWindow): # TODO: получать изображения прямо из интернета, не записывая в файл
    def __init__(self):
        super().__init__()

        self.spn_ind = 0

        self.static_api_params = {
            "l": "map",
            "ll": "30.416717,59.722324",
            "size": "650,450",
            "spn": "0.01,0.01"
        }

        uic.loadUi("../graphics/main_window.ui", self)
        self.setWindowTitle("Maps")
        self.setWindowIcon(QIcon("../graphics/maps.ico"))
        self.set_buttons()
        self.search()
        self.set_map_image()

    # обработка нажатия клавиш
    def keyPressEvent(self, event):
        # кнопка PageUp
        if event.key() == 0x01000016:
            self.spn_ind += 1
            if self.spn_ind == len(SPN):
                self.spn_ind -= 1
            else:
                self.static_api_params["spn"] = SPN[self.spn_ind]
                self.search()
        # кнопка PageDown
        elif event.key() == 0x01000017:
            self.spn_ind -= 1
            if self.spn_ind == -1:
                self.spn_ind = 0
            else:
                self.static_api_params["spn"] = SPN[self.spn_ind]
                self.search()

        # кнопка Left
        elif event.key() == 0x01000012:
            a, b = list(map(float, self.static_api_params["ll"].split(',')))
            a -= 0.01
            self.static_api_params["ll"] = f'{a},{b}'
            self.search()

        # кнопка Up
        elif event.key() == 0x01000013:
            a, b = list(map(float, self.static_api_params["ll"].split(',')))
            b += 0.01
            self.static_api_params["ll"] = f'{a},{b}'
            self.search()

        # кнопка Right
        elif event.key() == 0x01000014:
            a, b = list(map(float, self.static_api_params["ll"].split(',')))
            a += 0.01
            self.static_api_params["ll"] = f'{a},{b}'
            self.search()

        # кнопка Down
        elif event.key() == 0x01000015:
            a, b = list(map(float, self.static_api_params["ll"].split(',')))
            b -= 0.01
            self.static_api_params["ll"] = f'{a},{b}'
            self.search()


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
        self.static_api_params["l"] = "map"
        self.search()

    def set_satellite(self):
        self.static_api_params["l"] = "sat"
        self.search()

    def set_hybrid(self):
        self.static_api_params["l"] = "skl"
        self.search()

    def reset(self):
        pass

    def search(self):
        if self.adress_request.text():
            if get_coords(self.adress_request.text()):
                coords = get_coords(self.adress_request.text())
                self.static_api_params["ll"] = coords
                self.static_api_params["pt"] = f"{coords},pm2rdm"
        print(self.static_api_params)
        response = requests.get(MAP_API_SERVER, params=self.static_api_params)

        if response:
            print('static api response!')
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
