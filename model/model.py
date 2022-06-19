class Model:
    # singleton
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls._instance, cls):
            cls._instance = object.__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        self.broadcaster_list = []
        self.stream_list = []
        self.notify_cbk = None
        self.refresh_cbk = None

    def register_notify(self, cbk):
        self.notify_cbk = cbk

    def on_notify(self, stream_list):
        if callable(self.notify_cbk):
            for stm in stream_list:
                bro = self.find_broadcaster_by_id(stm.broadcaster_id)
                self.notify_cbk(stm, bro)

    def register_refresh(self, cbk):
        self.refresh_cbk = cbk

    def on_refresh(self):
        if callable(self.refresh_cbk):
            self.refresh_cbk()

    def refresh(self, broadcaster_list, stream_list):
        self.broadcaster_list = broadcaster_list
        self.stream_list = stream_list

    def find_broadcaster_by_id(self, id):
        for b in self.broadcaster_list:
            if b.id == id:
                return b
        return None
