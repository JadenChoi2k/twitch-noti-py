from PyQt6.QtWidgets import *
from PyQt6 import QtCore


class VerticalView(QWidget):
    def __init__(self):
        super().__init__()
        self.setLayout(self._create_layout())

    def _create_layout(self):
        layout = QVBoxLayout()
        layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        return layout

    def add(self, w):
        self.layout().addWidget(w)

    def delete_all(self):
        layout = self.layout()
        for idx in reversed(range(layout.count())):
            layout.itemAt(idx).widget().setParent(None)


if __name__ == '__main__':
    from widget.listwidget import streaming
    import sys
    app = QApplication(sys.argv)
    view = VerticalView()
    view.resize(700, 300)
    for i in range(10):
        view.add(streaming.example())
    view.show()
    sys.exit(app.exec())
