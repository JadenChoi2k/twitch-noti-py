from PyQt6.QtWidgets import *
from PyQt6 import QtCore
from PyQt6.QtCore import Qt
from PyQt6 import QtGui
from domain.broadcaster import BroadCaster
from domain.stream import Streaming
import urllib.request


def clickable(widget):
    class Filter(QtCore.QObject):
        clicked = QtCore.pyqtSignal()

        def eventFilter(self, obj, event):
            if obj == widget:
                if event.type() == QtCore.QEvent.Type.MouseButtonRelease:
                    if obj.rect().contains(event.pos()):
                        self.clicked.emit()
                        return True
            return False

    _filter = Filter(widget)
    widget.installEventFilter(_filter)
    return _filter.clicked


class Notification(QWidget):
    closed = QtCore.pyqtSignal(int)

    def __init__(self, broadcaster: BroadCaster, streaming: Streaming, size='medium'):
        super(Notification, self).__init__()
        self.index = None
        self.broadcaster, self.streaming, self.widget_size = broadcaster, streaming, size
        self.initUi()

    def initUi(self):
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.Tool)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setStyleSheet('background: transparent;')
        self.set_size(self.widget_size)

    def set_index(self, index):
        self.index = index

    def set_size(self, size):
        if size == 'small':
            self.set_small()
        elif size == 'large':
            self.set_medium()
        else:
            self.set_large()

    def set_small(self):
        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.setAlignment(Qt.AlignmentFlag.AlignRight)
        close_widget = QWidget()
        close_btn = QLabel()
        profile_widget = QLabel('profile here')
        # close button
        top_layout = QHBoxLayout()
        top_layout.setAlignment(Qt.AlignmentFlag.AlignRight)
        top_layout.setContentsMargins(0, 0, 0, 0)
        close_btn.setFixedSize(25, 25)
        close_btn.setScaledContents(True)
        pixmap = QtGui.QPixmap()
        pixmap.load('resources/x_icon_circle2.png')
        close_btn.setPixmap(pixmap)
        clickable(close_btn).connect(self.move_out)
        top_layout.addWidget(close_btn)
        close_widget.setLayout(top_layout)
        # profile
        profile_widget.setFixedSize(100, 100)
        profile_widget.setScaledContents(True)
        with urllib.request.urlopen(self.broadcaster.profile_url) as data:
            if data.status == 200:
                pixmap = QtGui.QPixmap()
                pixmap.loadFromData(data.read())
                # empty pixmap
                rounded = QtGui.QPixmap(pixmap.size())
                rounded.fill(QtGui.QColor("transparent"))
                # paint rounded pixmap
                with QtGui.QPainter(rounded) as painter:
                    painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)
                    painter.setBrush(QtGui.QBrush(pixmap))
                    painter.setPen(QtCore.Qt.PenStyle.NoPen)
                    painter.drawRoundedRect(rounded.rect(), rounded.width() // 2, rounded.height() // 2)
                profile_widget.setPixmap(rounded)
        clickable(profile_widget).connect(self.onclick)
        # assemble
        layout.addWidget(close_widget)
        layout.addWidget(profile_widget)
        self.setLayout(layout)

    def set_medium(self):
        layout = QHBoxLayout()
        # profile
        # name label

    def set_large(self):
        layout = QHBoxLayout()
        # close button
        # thumbnail
        # title label
        # game label
        # time label

    def move_to(self, dx, dy):
        self.move(self.x() + dx, self.y() + dy)

    # show
    # called by manager
    def move_in(self, x, y):
        self.move(x, y)
        self.show()

    # hide (close)
    # called by self
    def move_out(self):
        self.close()

    def onclick(self):
        self.open_browser()

    def open_browser(self):
        import webbrowser
        webbrowser.open(f'https://twitch.tv/{self.broadcaster.login_id}')
        self.move_out()

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.closed.emit(self.index)


def example(size):
    from datetime import datetime, timezone, timedelta
    _streaming = Streaming(49045679, '순대국 후로로루로루루로루로루로로록', 'Just Chatting',
                           'https://static-cdn.jtvnw.net/previews-ttv/live_user_woowakgood-{width}x{height}.jpg',
                           datetime(2022, 5, 21, 8, 56, 56).astimezone(timezone(timedelta(hours=9))))
    _broadcaster = BroadCaster(49045679, 'woowakgood', '우왁굳',
                               'https://static-cdn.jtvnw.net/jtv_user_pictures/ebc60c08-721b-4572-8f51-8be7136a0c96-profile_image-300x300.png')
    return Notification(_broadcaster, _streaming, size)


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    w = example('small')
    w.move_in(2430, 1250)
    sys.exit(app.exec())
