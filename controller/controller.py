from domain.apicaller import ApiCaller
from model.model import Model
model = Model()


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
        self.refetch()
        model.on_refresh()

    # just fetch again
    def refetch(self):
        broadcaster_list = self._fetch(self.apicaller.get_next_followed_broadcaster)
        stream_list = self._fetch(self.apicaller.get_next_followed_stream)
        model.refresh(broadcaster_list, stream_list)


    # monitor live-streaming and invoke model to notify if there exists new
    def monitor(self):
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
