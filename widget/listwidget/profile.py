from domain.broadcaster import BroadCaster
from PyQt6.QtWidgets import *
from PyQt6 import QtGui
from PyQt6 import QtCore
import urllib.request
import webbrowser
data_cache = {}


def get_profile_cache():
    global data_cache
    return data_cache


class ProfileWidget(QWidget):
    def __init__(self, broad_caster: BroadCaster, stream_on: bool = True):
        super().__init__()
        self.broadcaster = broad_caster
        self.stream_on = stream_on
        self.setToolTip(self.broadcaster.login_id)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setStyleSheet('QLabel {background: transparent;} QToolTip {background: white;}')
        self.setFixedSize(150, 180)
        vbox = QVBoxLayout()
        vbox.setContentsMargins(0, 0, 0, 0)
        self.profile_img = QLabel()
        self.profile_img.setScaledContents(True)
        self.set_profile_from_url(broad_caster.profile_url)
        self.name = QLabel(broad_caster.name)
        self.name.setAlignment(QtCore.Qt.AlignmentFlag.AlignVCenter | QtCore.Qt.AlignmentFlag.AlignHCenter)
        name_font = self.name.font()
        name_font.setPixelSize(18)
        self.name.setFont(name_font)
        vbox.addWidget(self.profile_img)
        vbox.addWidget(self.name)
        self.setLayout(vbox)

    def set_profile_from_url(self, url):
        global data_cache
        data = None
        if data_cache.get(url):
            data = data_cache[url]
        else:
            with urllib.request.urlopen(url) as fetch_data:
                if fetch_data.status == 200:
                    data = fetch_data.read()
                    data_cache[url] = data
        pixmap = QtGui.QPixmap()
        pixmap.loadFromData(data)
        if not self.stream_on:
            img = QtGui.QPixmap.toImage(pixmap)
            grayscale = img.convertToFormat(QtGui.QImage.Format.Format_Grayscale8)
            pixmap = QtGui.QPixmap.fromImage(grayscale)
        # empty pixmap
        rounded = QtGui.QPixmap(pixmap.size())
        rounded.fill(QtGui.QColor("transparent"))
        # paint rounded pixmap
        with QtGui.QPainter(rounded) as painter:
            painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)
            painter.setBrush(QtGui.QBrush(pixmap))
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.drawRoundedRect(rounded.rect(), rounded.width() // 2, rounded.height() // 2)
        self.profile_img.setPixmap(rounded)

    def mouseReleaseEvent(self, event: QtGui.QMouseEvent) -> None:
        if self.stream_on:
            if self.rect().contains(event.pos()):
                webbrowser.open(f'https://twitch.tv/{self.broadcaster.login_id}')


def example(stream_on=True):
    broadcaster = BroadCaster(1, 'zilioner', '?????????',
                              'https://static-cdn.jtvnw.net/jtv_user_pictures/dde955e8-5fae-44dc-98db-79b3b14afea2-profile_image-300x300.png')
    return ProfileWidget(broadcaster, stream_on)


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    profile_widget = example()
    profile_widget.show()
    app.exec()
