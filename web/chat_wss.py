# pylint: disable=missing-module-docstring
import sys

from gevent import pywsgi
from geventwebsocket.handler import WebSocketHandler

try:
    import wsgi # lively, chat_wss.py depends upon wsgi.py setup sys.path.
except ModuleNotFoundError:
    from web import wsgi

def main(app): # pylint: disable=missing-function-docstring
    wss = pywsgi.WSGIServer(('', app.config['WSS_PORT']), app, handler_class=WebSocketHandler)
    wss.serve_forever()
    return 0

if __name__ == '__main__':
    sys.exit(main(wsgi.create_app()))
