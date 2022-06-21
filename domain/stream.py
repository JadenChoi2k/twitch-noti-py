from datetime import datetime, timezone, timedelta
timezone_kst = timezone(timedelta(hours=9))


class Streaming:
    broadcaster_id: str = None
    title: str = None
    game_name: str = None
    thumbnail_url: str = None
    started_at: datetime = None

    def __init__(self, broadcaster_id, title, game_name, thumbnail_url, started_at):
        self.broadcaster_id = broadcaster_id
        self.title = title
        self.game_name = game_name
        self.thumbnail_url = thumbnail_url
        self.set_started_at(started_at)

    def set_started_at(self, started_at):
        if isinstance(started_at, str):
            print(started_at, end=' -> ')
            self.started_at = datetime.strptime(started_at, '%Y-%m-%dT%H:%M:%SZ').astimezone(timezone_kst)
            print(self.started_at)
        else:
            self.started_at = started_at

    def get_elapsed(self):
        return (datetime.utcnow().astimezone(timezone_kst) - self.started_at).seconds

    def get_image_url(self, width: int, height: int) -> str:
        return self.thumbnail_url.replace('{width}', str(width)).replace('{height}', str(height))

    def __str__(self) -> str:
        return f'broadcaster_id: {self.broadcaster_id}, title: {self.title},' \
               f' game_name: {self.game_name}, thumbnail_url: {self.thumbnail_url}, started_at: {self.started_at}'
