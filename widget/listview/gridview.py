from PyQt6 import QtGui
from PyQt6 import QtCore
from PyQt6.QtWidgets import *


class GridView(QWidget):
    spacing = 10
    content_margin = 10

    def __init__(self, item_width=150):
        super().__init__()
        self.item_width = 150
        self.pointer = 0, 0
        self.widgets = []
        self.rownum = self._calc_rownum(self.width())
        self.setup()

    def _create_layout(self):
        layout = QGridLayout()
        layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop | QtCore.Qt.AlignmentFlag.AlignJustify)
        layout.setSpacing(self.spacing)
        layout.setContentsMargins(self.content_margin, self.content_margin, self.content_margin, self.content_margin)
        return layout

    def setup(self):
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setStyleSheet('border: none; background: transparent;')
        self.setLayout(self._create_layout())

    def add(self, w):
        self.widgets.append(w)
        self._add_to_grid(w)

    def _add_to_grid(self, w, layout=None):
        if not layout:
            layout = self.layout()
        r, c = self.pointer
        if c >= self.rownum:
            r += 1
            c = 0
        c += 1
        self.pointer = r, c
        layout.addWidget(w, r, c)

    def delete_all(self):
        self.detach_all()
        for w in self.widgets:
            del w
        self.widgets = []

    def detach_all(self):
        layout = self.layout()
        for idx in reversed(range(layout.count())):
            layout.itemAt(idx).widget().setParent(None)
        self.pointer = 0, 0

    def update_status(self):
        pass

    def reassign(self):
        old_layout = self.layout()
        layout = self._create_layout()
        # self.detach_all()
        self.pointer = 0, 0
        for w in self.widgets:
            self._add_to_grid(w, layout)
        self.setLayout(layout)
        del old_layout

    def resizeEvent(self, event: QtGui.QResizeEvent) -> None:
        rownum = self._calc_rownum(event.size().width())
        if self.rownum != rownum:
            self.rownum = rownum
            self.reassign()
        if self._calc_rownum(event.size().width() - 1) == rownum - 1:
            self.rownum = rownum - 1
            self.reassign()
        super().resizeEvent(event)

    def _calc_rownum(self, width):
        return int((width - 2 * self.content_margin + self.spacing) / (self.item_width + self.spacing))


if __name__ == '__main__':
    from widget.listwidget import profile
    import sys
    app = QApplication(sys.argv)
    view = GridView()
    view.resize(700, 300)
    for i in range(15):
        view.add(profile.example(i % 3 == 0))
    view.show()
    sys.exit(app.exec())
