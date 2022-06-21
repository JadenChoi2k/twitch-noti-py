from domain.broadcaster import BroadCaster
from PyQt6.QtWidgets import *
from PyQt6 import QtGui
from PyQt6 import QtCore
import urllib.request


class ProfileWidget(QWidget):
    def __init__(self, broad_caster: BroadCaster, stream_on: bool = True):
        super().__init__()
        self.stream_on = stream_on
        self.setFixedSize(150, 180)
        vbox = QVBoxLayout()
        vbox.setContentsMargins(0, 0, 0, 0)
        self.profile_img = QLabel()
        self.profile_img.setScaledContents(True)
        self.set_profile_from_url(broad_caster.profile_url)
        self.name = QLabel(broad_caster.name)
        self.name.setAlignment(QtCore.Qt.AlignmentFlag.AlignVCenter | QtCore.Qt.AlignmentFlag.AlignHCenter)
        name_font = self.name.font()
        name_font.setPixelSize(15)
        self.name.setFont(name_font)
        vbox.addWidget(self.profile_img)
        vbox.addWidget(self.name)
        self.setLayout(vbox)

    def set_profile_from_url(self, url):
        with urllib.request.urlopen(url) as data:
            if data.status == 200:
                pixmap = QtGui.QPixmap()
                pixmap.loadFromData(data.read())
                if not self.stream_on:
                    img = QtGui.QPixmap.toImage(pixmap)
                    grayscale = img.convertToFormat(QtGui.QImage.Format.Format_Grayscale16)
                    pixmap = QtGui.QPixmap.fromImage(grayscale)
                # empty pixmap
                rounded = QtGui.QPixmap(pixmap.size())
                rounded.fill(QtGui.QColor("transparent"))
                # paint rounded pixmap
                painter = QtGui.QPainter(rounded)
                painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)
                painter.setBrush(QtGui.QBrush(pixmap))
                painter.setPen(QtCore.Qt.PenStyle.NoPen)
                painter.drawRoundedRect(rounded.rect(), rounded.width() // 2, rounded.height() // 2)
                self.profile_img.setPixmap(rounded)
            else:
                print('error from fetching profile image')


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    broadcaster = BroadCaster(1, 'login', '침착맨',
                              'https://static-cdn.jtvnw.net/jtv_user_pictures/dde955e8-5fae-44dc-98db-79b3b14afea2-profile_image-300x300.png')
    profile_widget = ProfileWidget(broadcaster, False)
    profile_widget.show()
    app.exec()
