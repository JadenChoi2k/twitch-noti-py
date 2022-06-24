from widget.notification.notification import Notification
from config.app.appconfig import AppConfiguration

config = AppConfiguration()
content_space = {'small': (140, 140), 'medium': (430, 130), 'large': (520, 150)}
# get display screen scale
SCREEN_SCALE = None
from ctypes import windll

LOGPIXELSX = 88
LOGPIXELSY = 90
user32 = windll.user32
user32.SetProcessDPIAware()
dc = user32.GetDC(0)
pix_per_inch = windll.gdi32.GetDeviceCaps(dc, LOGPIXELSX)
user32.ReleaseDC(0, dc)
SCREEN_SCALE = pix_per_inch * 0.0104


def _get_screen_size() -> tuple:
    global SCREEN_SCALE
    from win32api import GetSystemMetrics
    return int(GetSystemMetrics(61) / SCREEN_SCALE), int(GetSystemMetrics(62) / SCREEN_SCALE)


class NotificationManager:
    # singleton
    _instance = None
    widgets = []

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls._instance, cls):
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    # called by model
    # sets and shows notification widget
    def notify(self, broadcaster, streamer):
        size = config.get('notification', 'size')
        widget = Notification(broadcaster, streamer, size)
        widget.closed.connect(self.onclose)
        widget.set_index(len(self.widgets))
        cx, cy = widget.get_content_space()
        sx, sy = _get_screen_size()
        widget.move_in(sx - cx, sy - cy * (widget.index + 1) - 25)
        if config.get('notification', 'auto-open'):
            widget.open_browser()
        self.widgets.append(widget)

    def onclose(self, idx):
        cx, cy = self.widgets[idx].get_content_space()
        for i in range(idx + 1, len(self.widgets)):
            self.widgets[i].move_to(0, cy)
            self.widgets[i].index = i - 1
        del self.widgets[idx]


def example() -> tuple:
    from datetime import datetime, timezone, timedelta
    from domain.stream import Streaming
    from domain.broadcaster import BroadCaster
    return BroadCaster(49045679, 'woowakgood', '우왁굳',
                       'https://static-cdn.jtvnw.net/jtv_user_pictures/ebc60c08-721b-4572-8f51-8be7136a0c96-profile_image-300x300.png'), \
           Streaming(49045679, '순대국 후로로루로루루로루로루로로록', 'Just Chatting',
                     'https://static-cdn.jtvnw.net/previews-ttv/live_user_woowakgood-{width}x{height}.jpg',
                     datetime(2022, 5, 21, 8, 56, 56).astimezone(timezone(timedelta(hours=9))))


if __name__ == '__main__':
    import sys
    from PyQt6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    manager = NotificationManager()
    ex = example()
    for i in range(5):
        manager.notify(*ex)
    sys.exit(app.exec())
