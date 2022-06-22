import socket
from urllib import parse


def create_token_request_url(host='', response_type='token', client_id='',
                             redirect_uri='http://localhost:12355', scope=None):
    if scope is None:
        scope = []
    return f"{host}\
?response_type={response_type}\
&client_id={client_id}\
&redirect_uri={redirect_uri}\
&scope={parse.quote(' '.join(scope))}"


def _default_redirect_request_parser(data):
    spl = data.split(' ')[1][2:].split('&')
    rsc = {}
    for x in spl:
        name, val = x.split('=')
        rsc[name] = val
    return rsc


'''
listen to http request
use to get authorization token requested from twitch
after user 'authorizing' app, request start

host: response socket host
port: response socket port
cbk: callback function parses from data
'''
def listen_to_redirect(host: str = 'localhost', port: int = 3000, cbk=_default_redirect_request_parser):
    listening_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listening_socket.bind((host, port))
    listening_socket.listen(0)

    client_socket, addr = listening_socket.accept()
    # phase 1: redirect to url replaced '#' to '?'
    client_socket.recv(65535)
    client_socket.send('''HTTP/1.1 200 OK
Content-Length: 62
Content-Type: text/html

<script>location.href=location.href.replace("#","?");</script>'''.encode())
    # phase 2: receive data and close browser
    data = client_socket.recv(65535)
    client_socket.send('''HTTP/1.1 200 OK
Content-Length: 164
Content-Type: text/html

<script>
const closeWindow = function() {this.opener=this;window.close();}
closeWindow();
document.write('Authorization success. Please close the window');</script>'''.encode())
    client_socket.close()
    listening_socket.close()
    return cbk(data.decode())


if __name__ == '__main__':
    pass
