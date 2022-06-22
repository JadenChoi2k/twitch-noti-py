from config.app.appconfig import AppConfiguration
from widget.listview.verticalview import VerticalView
from widget.config.section import ConfigSectionWidget
from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt
config = AppConfiguration()


class ConfigurationPage(VerticalView):
    def __init__(self):
        super().__init__()
        self.setStyleSheet('''
        QPushButton {
            border: 1px solid #dedede;
            border-radius: 5px;
        }
        QPushButton:hover {
            transition: 1s;
            background: #f3f3f3;
        }
        ''')
        self.save_btn = QPushButton('저장')
        self.save_btn.clicked.connect(lambda: print('저장'))
        self.cancel_btn = QPushButton('취소')
        self.default_btn = QPushButton('기본값')
        self.setup()

    def setup(self):
        for sec, opt_dict in config.to_dict().items():
            self.add(ConfigSectionWidget(sec, opt_dict))
        bottom_widget = QWidget()
        bottom_layout = QHBoxLayout()
        bottom_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignRight)
        self.save_btn.setFixedSize(80, 30)
        self.save_btn.setEnabled(False)
        self.cancel_btn.setFixedSize(80, 30)
        self.default_btn.setFixedSize(80, 30)
        bottom_layout.addWidget(self.save_btn)
        bottom_layout.addWidget(self.cancel_btn)
        bottom_layout.addWidget(self.default_btn)
        bottom_widget.setLayout(bottom_layout)
        self.add(bottom_widget)


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    w = ConfigurationPage()
    w.resize(700, 500)
    w.show()
    sys.exit(app.exec())
