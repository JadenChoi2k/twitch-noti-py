class Model:
    # singleton
    _instance = None
    # instance field
    broadcaster_list = []
    stream_list = []
    notify_cbk = None
    refresh_cbk = None

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls._instance, cls):
            cls._instance = object.__new__(cls, *args, **kwargs)
        return cls._instance

    # cbk(broadcaster, streaming)
    def register_notify(self, cbk):
        self.notify_cbk = cbk

    def on_notify(self, stream_list):
        if callable(self.notify_cbk):
            for stm in stream_list:
                bro = self.find_broadcaster_by_id(stm.broadcaster_id)
                self.notify_cbk(bro, stm)

    def register_refresh(self, cbk):
        self.refresh_cbk = cbk

    def on_refresh(self):
        if callable(self.refresh_cbk):
            self.refresh_cbk()

    def refresh(self, broadcaster_list, stream_list):
        self.broadcaster_list = broadcaster_list
        self.stream_list = stream_list

    def find_broadcaster_by_id(self, broadcaster_id):
        for b in self.broadcaster_list:
            if b.id == broadcaster_id:
                return b
        return None

    def is_broadcaster_streaming(self, broadcaster_id) -> bool:
        for s in self.stream_list:
            if s.broadcaster_id == broadcaster_id:
                return True
        return False
