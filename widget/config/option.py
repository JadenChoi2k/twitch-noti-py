from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt
from PyQt6 import QtGui
from config.app.lang import resolver


class OptionWidget(QWidget):
    def __init__(self, name: str, values: list, value: int):
        super().__init__()
        self.name, self.values, self.value = name, values, value
        self.cbk = None
        self.name_lbl = QLabel(resolver.resolve(self.name))
        self.selection = QComboBox()
        self.initUi()

    def _create_layout(self):
        layout = QHBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(30, 10, 30, 10)
        return layout

    def initUi(self):
        layout = self._create_layout()
        # init name label
        self.name_lbl.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        self.name_lbl.setFont(QtGui.QFont('맑은 고딕', 15))
        # init selection combobox
        self.selection.setFixedHeight(30)
        self.selection.setStyleSheet('background: white;')
        self.selection.currentIndexChanged.connect(self._on_value_changed)
        for v in self.values:
            self.selection.addItem(resolver.resolve(v))
        self.selection.setCurrentIndex(self.value)
        # set layout
        layout.addWidget(self.name_lbl, 3)
        layout.addWidget(self.selection, 5)
        self.setLayout(layout)

    def get_value(self) -> int:
        return self.selection.currentIndex()

    def register_cbk(self, cbk):
        self.cbk = cbk

    def _on_value_changed(self):
        if callable(self.cbk):
            self.cbk(self.get_value())


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    w = OptionWidget('resolution', ['480 X 320', '760 X 480', '1024 X 576', '1280 X 720', '1600 X 900', '1920 X 1080'], 2)
    w.resize(500, 50)
    w.register_cbk(lambda x: print(x))
    w.show()
    sys.exit(app.exec())
