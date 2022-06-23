from domain.apicaller import ApiCaller
from model.model import Model
from PyQt6.QtCore import QThread, pyqtSignal
model = Model()
refresh_thread = None
monitoring_thread = None


class Controller:
    # singleton
    _instance = None
    # instance field
    apicaller: ApiCaller = None

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls._instance, cls):
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def init(self):
        self.apicaller = ApiCaller()

    # will be called by view layer, setup or refresh button
    def refresh(self):
        # self.refetch()
        # model.on_refresh()
        global refresh_thread
        refresh_thread = RefreshThread()
        refresh_thread.fetching_signal.connect(self.refetch)
        refresh_thread.model_refresh_signal.connect(model.on_refresh)
        refresh_thread.start()

    # just fetch again
    def refetch(self):
        broadcaster_list = self._fetch(self.apicaller.get_next_followed_broadcaster)
        stream_list = self._fetch(self.apicaller.get_next_followed_stream)
        model.refresh(broadcaster_list, stream_list)

    def monitor_start(self):
        global monitoring_thread
        monitoring_thread = MonitoringThread()
        monitoring_thread.monitoring_signal.connect(self._monitor)
        monitoring_thread.start()

    # monitor live-streaming and invoke model to notify if there exists new
    def _monitor(self):
        prev_streaming: list = model.stream_list
        next_streaming = self._fetch(self.apicaller.get_next_followed_stream)
        old_streaming, new_streaming = self._get_changes(prev_streaming, next_streaming)
        # if streaming changed
        if old_streaming or new_streaming:
            # if empty, nothing happens
            model.on_notify(new_streaming.values())
            model.refresh(model.broadcaster_list, next_streaming)
            model.on_refresh()

    def _get_changes(self, prev_streaming, next_streaming) -> tuple:
        prev_id_map = {prev.broadcaster_id: prev for prev in prev_streaming}
        next_id_map = {nxt.broadcaster_id: nxt for nxt in next_streaming}
        for pid in map(lambda s: s.broadcaster_id, prev_streaming):
            if next_id_map.get(pid):
                next_id_map.pop(pid)
        for nid in map(lambda s: s.broadcaster_id, next_streaming):
            if prev_id_map.get(nid):
                prev_id_map.pop(nid)
        return prev_id_map, next_id_map

    def _fetch(self, fetch_func):
        result = []
        is_end = False
        while not is_end:
            part, is_end = fetch_func()
            result += part
        return result


class RefreshThread(QThread):
    fetching_signal = pyqtSignal()
    model_refresh_signal = pyqtSignal()

    def __init__(self, parent=None):
        super(RefreshThread, self).__init__(parent)

    def run(self) -> None:
        self.fetching_signal.emit()
        self.model_refresh_signal.emit()


class MonitoringThread(QThread):
    monitoring_signal = pyqtSignal()

    def __init__(self, parent=None):
        from threading import Event
        super(MonitoringThread, self).__init__(parent)
        self.stopped = Event()

    def run(self) -> None:
        from config.app.appconfig import AppConfiguration
        config = AppConfiguration()
        while True:
            self.stopped.wait(config.get('system', 'refresh-interval'))
            self.monitoring_signal.emit()
