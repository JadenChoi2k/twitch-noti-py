from domain.stream import Streaming
from domain.broadcaster import BroadCaster
from PyQt6.QtWidgets import *
from PyQt6 import QtCore
from PyQt6 import QtGui
import urllib.request
import webbrowser
import datetime
data_cache = {}  # url: (data, datetime)


class StreamingWidget(QWidget):
    def __init__(self, streaming: Streaming, broadcaster: BroadCaster):
        super().__init__()
        self.streaming = streaming
        self.broadcaster = broadcaster
        self.setFixedHeight(120)
        self.thumbnail_image = self.fetch_thumbnail_image_url(streaming.get_image_url(400, 240))
        self.title = QLabel(f'[{broadcaster.name}] {streaming.title}')
        self.title.setMaximumWidth(800)
        self.title.setWordWrap(True)
        self.title.setFont(QtGui.QFont('맑은 고딕', 15))
        self.game_name = QLabel(streaming.game_name)
        self.game_name.setFont(QtGui.QFont('맑은 고딕', 15))
        self.streaming_time = QLabel(f'{streaming.get_elapsed() // 3600}h {streaming.get_elapsed() // 60 % 60}m')
        self.setup_layout()

    def fetch_thumbnail_image_url(self, url) -> QLabel:
        global data_cache
        lbl = QLabel()
        lbl.setScaledContents(True)
        lbl.setFixedSize(200, 120)
        data = None
        if data_cache.get(url):
            cached_data, _datetime = data_cache[url]
            if (datetime.datetime.now() - _datetime).seconds < 5 * 60:  # if cached time less than 5 minutes
                data = cached_data
        if data is None:
            with urllib.request.urlopen(url) as fetch_data:
                data = fetch_data.read()
                data_cache[url] = (data, datetime.datetime.now())
        pixmap = QtGui.QPixmap()
        pixmap.loadFromData(data)
        rounded = QtGui.QPixmap(pixmap.size())
        rounded.fill(QtGui.QColor("transparent"))
        with QtGui.QPainter(rounded) as painter:
            painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)
            painter.setBrush(QtGui.QBrush(pixmap))
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.drawRoundedRect(rounded.rect(), 15, 15)
        lbl.setPixmap(rounded)
        return lbl

    def setup_layout(self):
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(self.thumbnail_image)
        mid_layout = QVBoxLayout()
        mid_layout.addWidget(self.title)
        mid_layout.addWidget(self.game_name)
        main_layout.addSpacing(20)
        main_layout.addLayout(mid_layout)
        main_layout.addStretch(1)
        right_layout = QVBoxLayout()
        right_layout.addStretch(1)
        right_layout.addWidget(self.streaming_time)
        right_layout.addSpacing(10)
        main_layout.addLayout(right_layout)
        main_layout.addSpacing(10)
        self.setLayout(main_layout)

    def update_time(self):
        self.streaming_time.setText(f'{self.streaming.get_elapsed() // 3600}h {self.streaming.get_elapsed() % 3600}m')

    def eventFilter(self, obj, event: QtCore.QEvent) -> bool:
        print('event filter', event)
        if event.type() == QtCore.QEvent.Type.HoverEnter:
            print('hover')
        return super(StreamingWidget, self).eventFilter(obj, event)

    def mouseReleaseEvent(self, event: QtGui.QMouseEvent) -> None:
        if self.rect().contains(event.pos()):
            webbrowser.open(f'https://twitch.tv/{self.broadcaster.login_id}')

    def on_mouse_enter(self):
        print('enter')
        self.setStyleSheet('background-color: black')


def example():
    from datetime import datetime, timezone, timedelta
    _streaming = Streaming(49045679, '순대국 후로로루로루루로루로루로로록', 'Just Chatting', 'https://static-cdn.jtvnw.net/previews-ttv/live_user_woowakgood-{width}x{height}.jpg', datetime(2022, 5, 21, 8, 56, 56).astimezone(timezone(timedelta(hours=9))))
    _broadcaster = BroadCaster(49045679, 'woowakgood', '우왁굳', 'https://static-cdn.jtvnw.net/jtv_user_pictures/ebc60c08-721b-4572-8f51-8be7136a0c96-profile_image-300x300.png')
    return StreamingWidget(_streaming, _broadcaster)


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    stream_widget = example()
    stream_widget.show()
    app.exec()
