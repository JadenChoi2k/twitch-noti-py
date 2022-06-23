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
        self.option_widget_list = []
        self.change_count = 0
        self.change_cbk = None
        self.initUi()

    def initUi(self):
        layout = self._create_layout()
        self.name_lbl.setFont(QtGui.QFont('맑은 고딕', 20))
        layout.addWidget(self.name_lbl)
        for k, v in self.option_dict.items():
            option_widget = OptionWidget(k, APP_CONFIG_CONSTANTS[self.section_name][k], v)
            option_widget.register_change_cbk(self.option_value_changed)
            self.option_widget_list.append(option_widget)
            layout.addWidget(option_widget)
        self.setLayout(layout)

    def _create_layout(self) -> QVBoxLayout:
        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        return layout

    # change_cbk(plus_count: bool)
    def register_change_cbk(self, cbk):
        self.change_cbk = cbk

    def option_value_changed(self, is_changed: bool):
        self.change_count += 1 if is_changed else -1
        # print(f'section {self.section_name} change_count = {self.change_count}')
        if not callable(self.change_cbk):
            return
        if self.change_count == 1 and is_changed:
            self.change_cbk(True)
        elif self.change_count == 0:
            self.change_cbk(False)

    def save_values(self) -> dict:
        self.change_count = 0
        return {opt_wdt.name: opt_wdt.save_value() for opt_wdt in self.option_widget_list}


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    w = ConfigSectionWidget('system', APP_DEFAULT_SETTINGS['system'])
    w.resize(700, 500)
    w.show()
    sys.exit(app.exec())
