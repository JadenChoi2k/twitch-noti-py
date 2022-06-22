import sys
import os
from PyQt6.QtWidgets import *
from PyQt6 import QtCore
from PyQt6 import uic
from config.app.appconfig import AppConfiguration
from controller.controller import Controller
from model.model import Model
from widget.listview.followlist import FollowList
from widget.listview.streamlist import StreamList

controller = Controller()
model = Model()
config = AppConfiguration()
title_ui = None
if os.path.isfile('main.ui'):
    title_ui = uic.loadUiType('main.ui')[0]
else:
    title_ui = uic.loadUiType('widget/main.ui')[0]
while not title_ui:
    continue


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
    followed_list: FollowList = None
    followed_scroll: QScrollArea = None  # page 0
    streaming_list: StreamList = None
    streaming_scroll: QScrollArea = None  # page 1
    option_scroll: QScrollArea = None  # page 2
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
        # init widgets
        self.followed_list = FollowList()
        self.streaming_list = StreamList()
        # setup buttons
        self.btn_start.clicked.connect(self.to_loading_page)
        self.btn_followed.clicked.connect(lambda: self.stk_view.setCurrentIndex(0))
        self.btn_streaming.clicked.connect(lambda: self.stk_view.setCurrentIndex(1))
        self.btn_option.clicked.connect(lambda: self.stk_view.setCurrentIndex(2))
        self.btn_background.clicked.connect(lambda: print('to background'))
        # setup view widgets to scroll
        self.followed_scroll.setWidget(self.followed_list)
        self.streaming_scroll.setWidget(self.streaming_list)
        # setup callback functions
        model.register_refresh(self._on_refresh)
        model.register_notify(lambda x: print(x))

    def to_title_page(self):
        self.stk_main.setCurrentIndex(0)

    def to_loading_page(self):
        global controller
        self.lbl_loading.setText('트위치 서버에 연결 중...')
        self.stk_main.setCurrentIndex(1)
        t = ControllerLoading(self)
        t.on_load_end.connect(self._on_load_end)
        t.start()

    def _on_load_end(self):
        controller.refresh()
        self.to_main_page()

    def _on_refresh(self):
        self.followed_list.delete_all()
        self.streaming_list.delete_all()
        # add broadcaster
        broadcaster_list = []
        for b in model.broadcaster_list:
            broadcaster_list.append((b, model.is_broadcaster_streaming(b.id)))
        broadcaster_list.sort(key=lambda x: x[1], reverse=True)
        for t in broadcaster_list:
            self.followed_list.add_follow_item(*t)
        for w in self.followed_list.widgets:
            w.setParent(self.followed_list)
        # add streaming
        for s in model.stream_list:
            self.streaming_list.add_stream_item(s, model.find_broadcaster_by_id(s.broadcaster_id))

    def to_main_page(self):
        # controller.refresh()
        self.stk_main.setCurrentIndex(2)

    def to_error_page(self, error_msg):
        self.stk_main.setCurrentIndex(3)


class ControllerLoading(QtCore.QThread):
    on_load_end = QtCore.pyqtSignal()

    def __init__(self, parent):
        super().__init__(parent)
        self.parent: MainWindow = parent

    def run(self):
        _controller = Controller()
        _controller.init()
        self.on_load_end.emit()


def execute():
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    execute()