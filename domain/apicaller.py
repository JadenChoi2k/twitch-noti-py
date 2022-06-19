from api.apihelper import TwitchApiHelper
from domain.broadcaster import BroadCaster
from domain.stream import Streaming


class ApiCaller:
    def __init__(self):
        self.th = TwitchApiHelper()

    def get_next_followed_broadcaster(self) -> tuple:
        channel_info_list, is_end = self.th.paging_follow_channel_info()
        broadcaster_info_list = self.th.get_broadcaster_info(channel_info_list)
        return [BroadCaster(bi['id'], bi['login'], bi['display_name'], bi['profile_image_url'])
                for bi in broadcaster_info_list], is_end

    def get_next_followed_stream(self) -> tuple:
        stream_list, is_end, = self.th.paging_stream_followed()
        return list(map(lambda x: Streaming(x['user_id'], x['title'], x['game_name'], x['thumbnail_url'], x['started_at']),
                        stream_list)), is_end
