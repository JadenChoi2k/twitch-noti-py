import webbrowser
from api import authorize
from api.const import CLIENT_ID, REDIRECT_PORT, AUTHORIZE_HOST, RESOURCE_SCOPE


class AuthorizeHelper:
    def __init__(self, client_id=CLIENT_ID):
        self.client_id = client_id
        self.access_token = None

    def authorize_and_get_token_info(self) -> dict:
        port = REDIRECT_PORT
        redirect_uri = f'http://localhost:{port}'
        request_url = authorize.create_token_request_url(
            host=AUTHORIZE_HOST, client_id=self.client_id, redirect_uri=redirect_uri, scope=RESOURCE_SCOPE)
        webbrowser.open(request_url)
        token_info = authorize.listen_to_redirect(port=port)
        self.access_token = token_info['access_token']
        return token_info

    def get_access_token(self):
        return self.access_token


if __name__ == '__main__':
    pass
