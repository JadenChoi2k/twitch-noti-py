import sys
import os
from PyQt6.QtWidgets import *
from PyQt6 import uic
from config.app.appconfig import AppConfiguration
from controller.controller import Controller

controller = Controller()
config = AppConfiguration()
title_ui = None
if os.path.isfile('main.ui'):
    title_ui = uic.loadUiType('main.ui')[0]
else:
    title_ui = uic.loadUiType('widget/main.ui')[0]


class MainWindow(QMainWindow, title_ui):
    # page stacked widget
    stk_main: QStackedWidget = None
    # page 0 widgets
    lbl_title_logo: QLabel = None
    btn_start: QPushButton = None
    lbl_version_info: QLabel = None
    lbl_github_info: QLabel = None
    # page 1 widgets
    lbl_loading: QLabel = None
    # page 2 widgets
    # left navigation sidebar
    lbl_nav_logo: QLabel = None
    btn_followed: QPushButton = None
    btn_streaming: QPushButton = None
    btn_option: QPushButton = None
    btn_background: QPushButton = None
    # right view
    stk_view: QStackedWidget = None
    page_0_followed: QWidget = None
    page_1_streaming: QWidget = None
    page_2_option: QWidget = None
    # page 3 widgets
    lbl_error: QLabel = None

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setup()
        self.to_title_page()

    def setup(self):
        # setup window
        self.resize(*config.get('system', 'resolution'))
        # setup buttons
        self.btn_start.clicked.connect(self.to_loading_page)
        self.btn_followed.clicked.connect(lambda: self.stk_view.setCurrentIndex(0))
        self.btn_streaming.clicked.connect(lambda: self.stk_view.setCurrentIndex(1))
        self.btn_option.clicked.connect(lambda: self.stk_view.setCurrentIndex(2))
        self.btn_background.clicked.connect(lambda: print('to background'))

    def to_title_page(self):
        self.stk_main.setCurrentIndex(0)

    def to_loading_page(self, loading_comment: str):
        global controller
        self.stk_main.setCurrentIndex(1)
        controller.init()
        self.to_main_page()

    def to_main_page(self):
        self.stk_main.setCurrentIndex(2)

    def to_error_page(self, error_msg):
        self.stk_main.setCurrentIndex(3)


def execute():
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    app.exec()


if __name__ == '__main__':
    execute()
