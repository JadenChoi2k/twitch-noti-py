from requests import get
from api.authhelper import AuthorizeHelper
from api.const import API_HOST, CLIENT_ID


class TwitchApiHelper:
    _auth_helper = None
    _headers = None
    _my_id = None
    _paging_follow_cursor = None
    _paging_stream_follow_cursor = None

    def __init__(self):
        self._auth_helper = AuthorizeHelper()
        self._update_variables()

    def _update_variables(self):
        self._update_headers()
        self._update_my_id_if_nonexistent()

    def _update_headers(self):
        self._auth_helper.authorize_and_get_token_info()
        self._headers = {'Client-Id': CLIENT_ID, 'Authorization': f'Bearer {self._auth_helper.get_access_token()}'}

    def _update_my_id_if_nonexistent(self):
        if not self._my_id:
            self.get_me()

    # returns my info
    def get_me(self):
        resp = get(f'{API_HOST}/users', headers=self._headers)
        json_resp = resp.json()
        self._my_id = json_resp['data'][0]['id']
        return json_resp['data']

    # paging follow
    # returns (data, whether paging ended)
    def paging_follow(self) -> tuple:
        self._update_my_id_if_nonexistent()
        url = f'{API_HOST}/users/follows?from_id={self._my_id}' \
              + (f'&after={self._paging_follow_cursor}' if self._paging_follow_cursor else '')
        resp = get(url, headers=self._headers)
        json_resp = resp.json()
        self._paging_follow_cursor = json_resp['pagination'].get('cursor')
        return json_resp['data'], self._paging_follow_cursor is None

    # paging followed channel info
    # returns (data, whether paging ended)
    def paging_follow_channel_info(self) -> tuple:
        page, is_end = self.paging_follow()
        channel_info_page = self.get_channel_info(list(map(lambda x: x['to_id'], page)))
        return channel_info_page, is_end

    # paging streams of followed
    # returns (data, whether paging ends)
    def paging_stream_followed(self) -> tuple:
        self._update_my_id_if_nonexistent()
        url = f'{API_HOST}/streams/followed?user_id={self._my_id}' \
              + (f'&after={self._paging_stream_follow_cursor}' if self._paging_stream_follow_cursor else '')
        resp = get(url, headers=self._headers)
        json_resp = resp.json()
        self._paging_stream_follow_cursor = json_resp['pagination'].get('cursor')
        return json_resp['data'], self._paging_stream_follow_cursor is None

    def get_channel_info(self, broadcaster_id_list: list) -> list:
        if len(broadcaster_id_list) > 100:
            return self.get_channel_info(broadcaster_id_list[:100]) + self.get_channel_info(broadcaster_id_list[100:])
        resp = get(f'{API_HOST}/channels?{"&".join(map(lambda x: f"broadcaster_id={x}", broadcaster_id_list))}',
                   headers=self._headers)
        return resp.json()['data']

    def get_user_info(self, user_id_list: list) -> list:
        if len(user_id_list) > 100:
            return self.get_user_info(user_id_list[:100]) + self.get_user_info(user_id_list[100:])
        resp = get(f'{API_HOST}/users?{"&".join(map(lambda x: f"id={x}", user_id_list))}',
                   headers=self._headers)
        return resp.json()['data']

    def get_broadcaster_info(self, channel_info_list: list) -> list:
        return self.get_user_info([ch['broadcaster_id'] for ch in channel_info_list])

    # open live stream of streamer
    def open_stream(self, broadcaster_login: str):
        import webbrowser
        webbrowser.open(f'https://www.twitch.tv/{broadcaster_login}')

    def open_stream_by_id(self, broadcaster_id: int):
        channel_info = self.get_channel_info([broadcaster_id])[0]
        self.open_stream(channel_info.get('broadcaster_login'))
