from domain.apicaller import ApiCaller
from model.model import Model
model = Model()


class Controller:
    # singleton
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls._instance, cls):
            cls._instance = object.__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        self.apicaller = ApiCaller()

    def on_refresh(self):
        broadcaster_list, stream_list = [], []
        is_end = False
        while not is_end:
            broadcaster, is_end = self.apicaller.get_next_followed_broadcaster()
            broadcaster_list += broadcaster
        is_end = False
        while not is_end:
            stream, is_end, = self.apicaller.get_next_followed_stream()
            stream_list += stream
        model.refresh(broadcaster_list, stream_list)
        model.on_refresh()

