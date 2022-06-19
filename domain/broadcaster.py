class BroadCaster:
    id: str = None
    login_id: str = None
    name: str = None
    profile_url: str = None

    def __init__(self, id, login_id, name, profile_url):
        self.id = id
        self.login_id = login_id
        self.name = name
        self.profile_url = profile_url

    def __str__(self) -> str:
        return f'id: {self.id}, login_id: {self.login_id}, name: {self.name}, profile_url: {self.profile_url}'
