from widget.listview.gridview import GridView
from widget.listwidget.profile import ProfileWidget
from domain.broadcaster import BroadCaster


class FollowList(GridView):
    def __init__(self):
        super(FollowList, self).__init__()

    def add_follow_item(self, b: BroadCaster, on: bool):
        self.add(ProfileWidget(b, on))
