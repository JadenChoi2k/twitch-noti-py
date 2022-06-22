from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt
from PyQt6 import QtGui
from widget.config.option import OptionWidget
from config.app.lang import resolver
from config.app.const import APP_CONFIG_CONSTANTS, APP_DEFAULT_SETTINGS


class ConfigSectionWidget(QWidget):
    def __init__(self, section_name: str, option_dict: dict):
        super().__init__()
        self.section_name, self.option_dict = section_name, option_dict
        self.name_lbl = QLabel(resolver.resolve(section_name))
        self.initUi()

    def initUi(self):
        layout = self._create_layout()
        self.name_lbl.setFont(QtGui.QFont('맑은 고딕', 20))
        layout.addWidget(self.name_lbl)
        for k, v in self.option_dict.items():
            layout.addWidget(OptionWidget(k, APP_CONFIG_CONSTANTS[self.section_name][k], v))
        self.setLayout(layout)

    def _create_layout(self) -> QVBoxLayout:
        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        return layout


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    w = ConfigSectionWidget('system', APP_DEFAULT_SETTINGS['system'])
    w.resize(700, 500)
    w.show()
    sys.exit(app.exec())
