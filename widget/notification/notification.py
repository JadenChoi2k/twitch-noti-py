from PyQt6.QtWidgets import *
from PyQt6 import QtCore
from PyQt6.QtCore import Qt
from PyQt6 import QtGui
from domain.broadcaster import BroadCaster
from domain.stream import Streaming
import urllib.request
import os
from widget.listwidget import profile
from config.app.appconfig import AppConfiguration

config = AppConfiguration()


def get_path_from_current(*args):
    return os.path.join(os.path.dirname(__file__), *args)


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
        t = ClosingThread(config.get('notification', 'move-out-time'), self)
        t.closing.connect(self.move_out)
        t.start()

    def initUi(self):
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.Tool)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setStyleSheet('background: transparent;')
        self.resize(400, 100)
        self.set_size(self.widget_size)

    def set_index(self, index):
        self.index = index

    def set_size(self, size):
        if size == 'small':
            self.set_small()
            # self.resize(150, 100)
            self.setFixedSize(180, 140)
        elif size == 'medium':
            self.set_medium()
            self.setFixedSize(400, 120)
        else:
            self.set_large()
            self.setFixedSize(500, 135)

    def set_small(self):
        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.setAlignment(Qt.AlignmentFlag.AlignRight)
        close_widget = QWidget()
        close_btn = self._create_close_button()
        profile_widget = self._create_profile_widget()
        # close button
        top_layout = QHBoxLayout()
        top_layout.setAlignment(Qt.AlignmentFlag.AlignRight)
        top_layout.setContentsMargins(0, 0, 0, 0)
        top_layout.addWidget(close_btn)
        close_widget.setLayout(top_layout)
        # assemble
        layout.addWidget(close_widget)
        layout.addWidget(profile_widget)
        self.setLayout(layout)

    def set_medium(self):
        _layout = QVBoxLayout()
        _layout.setContentsMargins(0, 0, 0, 0)
        _layout.setSpacing(0)
        _widget = QWidget()
        effect = QGraphicsOpacityEffect()
        effect.setOpacity(0.9)
        _widget.setGraphicsEffect(effect)
        layout = QHBoxLayout()
        layout.setContentsMargins(6, 10, 10, 10)
        self.setStyleSheet('background: #fafafa; border-radius: 10px;')
        profile_widget = self._create_profile_widget()
        title_label = QLabel(f'[{self.broadcaster.name}] {self.streaming.title}')
        playing_game_label = QLabel(f'{self.streaming.game_name} 플레이 중')
        close_btn = self._create_close_button()
        # description_label
        description_widget = QWidget()
        description_layout = QVBoxLayout()
        description_layout.setContentsMargins(0, 0, 0, 0)
        description_layout.setSpacing(0)
        title_label.setWordWrap(True)
        title_label.setMaximumWidth(240)
        title_label.setFont(QtGui.QFont('맑은 고딕', 12))
        playing_game_label.setMaximumWidth(240)
        playing_game_label.setFont(QtGui.QFont('맑은 고딕', 12))
        description_layout.addWidget(title_label)
        description_layout.addStretch(1)
        description_layout.addWidget(playing_game_label)
        description_widget.setLayout(description_layout)
        clickable(description_widget).connect(self.onclick)
        # close_btn
        close_layout = QVBoxLayout()
        close_layout.setContentsMargins(0, 0, 0, 0)
        close_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        close_layout.addWidget(close_btn)
        # assemble
        layout.addWidget(profile_widget)
        layout.addWidget(description_widget)
        layout.addLayout(close_layout)
        _widget.setLayout(layout)
        _layout.addWidget(_widget)
        self.setLayout(_layout)

    def set_large(self):
        _layout = QVBoxLayout()
        _layout.setContentsMargins(0, 0, 0, 0)
        _layout.setSpacing(0)
        _widget = QWidget()
        effect = QGraphicsOpacityEffect()
        effect.setOpacity(0.9)
        _widget.setGraphicsEffect(effect)
        layout = QHBoxLayout()
        layout.setContentsMargins(8, 8, 5, 8)
        self.setStyleSheet('background: #fafafa; border-radius: 10px;')
        profile_widget = self._create_thumbnail_widget()
        title_label = QLabel(f'[{self.broadcaster.name}] {self.streaming.title}')
        playing_game_label = QLabel(f'{self.streaming.game_name} 플레이 중')
        close_btn = self._create_close_button()
        # description_label
        description_widget = QWidget()
        description_layout = QVBoxLayout()
        title_label.setWordWrap(True)
        title_label.setMaximumWidth(240)
        title_label.setFont(QtGui.QFont('맑은 고딕', 12))
        playing_game_label.setMaximumWidth(240)
        playing_game_label.setFont(QtGui.QFont('맑은 고딕', 12))
        description_layout.addWidget(title_label)
        description_layout.addStretch(1)
        description_layout.addWidget(playing_game_label)
        description_widget.setLayout(description_layout)
        clickable(description_widget).connect(self.onclick)
        # close_btn
        close_layout = QVBoxLayout()
        close_layout.setContentsMargins(0, 0, 0, 0)
        close_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        close_layout.addWidget(close_btn)
        # assemble
        layout.addWidget(profile_widget)
        layout.addWidget(description_widget)
        layout.addLayout(close_layout)
        _widget.setLayout(layout)
        _layout.addWidget(_widget)
        self.setLayout(_layout)

    def _create_profile_widget(self):
        cache = profile.get_profile_cache()
        profile_widget = QLabel('profile here')
        profile_widget.setFixedSize(100, 100)
        profile_widget.setScaledContents(True)
        data = None
        url = self.broadcaster.profile_url
        if cache.get(url):
            data = cache[url]
        else:
            with urllib.request.urlopen(url) as fetch_data:
                if fetch_data.status == 200:
                    data = fetch_data.read()
        pixmap = QtGui.QPixmap()
        pixmap.loadFromData(data)
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
        return profile_widget

    def _create_close_button(self):
        close_btn = QLabel()
        close_btn.setFixedSize(25, 25)
        close_btn.setScaledContents(True)
        pixmap = QtGui.QPixmap()
        pixmap.load(get_path_from_current('resources', 'x_icon_circle2.png'))
        close_btn.setPixmap(pixmap)
        clickable(close_btn).connect(self.move_out)
        return close_btn

    def _create_thumbnail_widget(self):
        profile_widget = QLabel('profile here')
        profile_widget.setFixedSize(200, 120)
        profile_widget.setScaledContents(True)
        with urllib.request.urlopen(self.streaming.get_image_url(400, 240)) as data:
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
                    painter.drawRoundedRect(rounded.rect(), 8, 8)
                profile_widget.setPixmap(rounded)
        clickable(profile_widget).connect(self.onclick)
        return profile_widget

    def get_content_space(self) -> tuple:
        return self.width() + 25, self.height() + 5

    def move_to(self, dx, dy, sec=1):
        animation = config.get('notification', 'animation')
        sx, sy = self.x(), self.y()
        ex, ey = sx + dx, sy + dy
        if animation == 'OFF':
            self.move(self.x() + dx, self.y() + dy)
            return
        self.anim_mv = QtCore.QPropertyAnimation(self, b"pos")
        self.anim_mv.setEasingCurve(self._get_animation_curve(animation))
        self.anim_mv.setDuration(int(sec * 1000))
        self.anim_mv.setStartValue(QtCore.QPoint(self.x(), self.y()))
        self.anim_mv.setEndValue(QtCore.QPoint(ex, ey))
        self.anim_mv.start()

    # show
    # called by manager
    def move_in(self, x, y):
        sec = 0.5
        sx, sy = x + self.width() + 50, y
        animation = config.get('notification', 'animation')
        if animation == 'OFF':
            self.move(x, y)
            self.show()
            return
        self.move(sx, sy)
        self.move_to(-(self.width() + 50), 0, sec)
        self.show()

    # hide (close)
    # called by self
    def move_out(self):
        sec = 0.25
        animation = config.get('notification', 'animation')
        if animation == 'OFF':
            self.close()
            return
        self.move_to(self.width() + 50, 0, sec)
        self.move_out_close_t = ClosingThread(sec + 0.1, self)
        self.move_out_close_t.closing.connect(self.close)
        self.move_out_close_t.start()

    def _get_animation_curve(self, animation):
        if animation == 'ENERGETIC':
            return QtCore.QEasingCurve.Type.InOutExpo
        elif animation == 'BOUND':
            return QtCore.QEasingCurve.Type.InOutBack
        elif animation == 'SMOOTH':
            return QtCore.QEasingCurve.Type.InOutSine

    def onclick(self):
        self.open_browser()
        self.move_out()

    def open_browser(self):
        import webbrowser
        webbrowser.open(f'https://twitch.tv/{self.broadcaster.login_id}')

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.closed.emit(self.index)


class ClosingThread(QtCore.QThread):
    closing = QtCore.pyqtSignal()

    def __init__(self, sec, parent=None):
        super(ClosingThread, self).__init__(parent)
        self.parent = parent
        self.sec = sec

    def run(self) -> None:
        import time
        if self.sec > 0:
            time.sleep(self.sec)
            self.closing.emit()


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
    w = example('medium')
    w.move_in(2150, 1250)
    sys.exit(app.exec())
