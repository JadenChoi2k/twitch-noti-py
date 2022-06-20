import sys
from PyQt6.QtWidgets import *
from PyQt6 import uic
from config.app.appconfig import AppConfiguration

config = AppConfiguration()
title_ui = uic.loadUiType('main.ui')[0]


class MainWindow(QMainWindow, title_ui):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.resize(*config.get('system', 'resolution'))


def execute():
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    app.exec()


if __name__ == '__main__':
    execute()
