from widget.listview.verticalview import VerticalView
from widget.listwidget.streaming import StreamingWidget
from domain.stream import Streaming
from domain.broadcaster import BroadCaster


class StreamList(VerticalView):
    def __init__(self):
        super().__init__()

    def add_stream_item(self, s: Streaming, b: BroadCaster):
        if s and b:
            self.add(StreamingWidget(s, b))
