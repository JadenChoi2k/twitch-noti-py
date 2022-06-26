from config.app.appconfig import AppConfiguration
from widget.listview.verticalview import VerticalView
from widget.config.section import ConfigSectionWidget
from config.app.const import APP_DEFAULT_SETTINGS
from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6 import QtGui
config = AppConfiguration()


class ConfigurationPage(VerticalView):
    changed = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setStyleSheet('''
        QPushButton {
            border: 1px solid #dedede;
            border-radius: 5px;
        }
        QPushButton:hover {
            background: #f3f3f3;
        }
        QPushButton:focus {
            background: #fafafa;
        }
        ''')
        self.section_widget_list = []
        self.change_count = 0
        self.save_btn = QPushButton('저장')
        self.cancel_btn = QPushButton('취소')
        self.default_btn = QPushButton('기본값')
        self.setup()

    def setup(self):
        for sec, opt_dict in config.to_dict().items():
            section_widget = ConfigSectionWidget(sec, opt_dict)
            section_widget.register_change_cbk(self.on_change)
            self.section_widget_list.append(section_widget)
            self.add(section_widget)
        bottom_widget = QWidget()
        bottom_layout = QHBoxLayout()
        bottom_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignRight)
        self.save_btn.setFont(QtGui.QFont('맑은 고딕', 12))
        self.cancel_btn.setFont(QtGui.QFont('맑은 고딕', 12))
        self.default_btn.setFont(QtGui.QFont('맑은 고딕', 12))
        self.save_btn.setFixedSize(90, 35)
        self.save_btn.setEnabled(False)
        self.cancel_btn.setFixedSize(90, 35)
        self.cancel_btn.setEnabled(False)
        self.default_btn.setFixedSize(90, 35)
        self.save_btn.clicked.connect(self.on_save_click)
        self.cancel_btn.clicked.connect(self.on_cancel_click)
        self.default_btn.clicked.connect(self.on_default_click)
        bottom_layout.addWidget(self.save_btn)
        bottom_layout.addWidget(self.cancel_btn)
        bottom_layout.addWidget(self.default_btn)
        bottom_widget.setLayout(bottom_layout)
        self.add(bottom_widget)

    def on_change(self, plus_count: bool):
        self.change_count += 1 if plus_count else -1
        # print(f'page change_count = {self.change_count}')
        if self.change_count > 0:
            self.save_btn.setEnabled(True)
            self.cancel_btn.setEnabled(True)
        else:
            self.save_btn.setEnabled(False)
            self.cancel_btn.setEnabled(False)

    def on_save_click(self):
        config.update({sec_wdt.section_name: sec_wdt.save_values() for sec_wdt in self.section_widget_list})
        config.save()
        self.change_count = 0
        self.save_btn.setEnabled(False)
        self.cancel_btn.setEnabled(False)
        self.changed.emit()

    def on_cancel_click(self):
        for sec in self.section_widget_list:
            for opt in sec.option_widget_list:
                opt.cancel_option()

    def on_default_click(self):
        # 1. set to default values
        for sec in self.section_widget_list:
            for opt in sec.option_widget_list:
                opt.change_value(APP_DEFAULT_SETTINGS[sec.section_name][opt.name])
        # 2. click save button (method)
        self.on_save_click()


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    w = ConfigurationPage()
    w.resize(700, 500)
    w.show()
    sys.exit(app.exec())
