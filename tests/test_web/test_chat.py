# pylint: disable=missing-module-docstring
import contextlib
import json
import multiprocessing
import time

import gevent
import gevent.monkey
import websocket

import test_app # pylint: disable=import-error
                # It should be the first imported module as the sys.path init in it.

import web.chat
import web.chat_wss

@contextlib.contextmanager
def serve_wss(app):
    '''Starts a ws server.'''
    gevent.monkey.patch_subprocess()

    proc = multiprocessing.Process(target=web.chat_wss.main, args=(app,))
    proc.start()

    try:
        yield
    finally:
        proc.terminate()

@contextlib.contextmanager
def get_connect_fn():
    '''Serves a ws server for unit testing.'''

    @contextlib.contextmanager
    def connect():
        ws = websocket.WebSocket() # pylint: disable=invalid-name

        for i in range(1, 3):
            try:
                ws.connect('ws://127.0.0.1:5001/chats/')
            except ConnectionRefusedError:
                sec = i % 3
                if sec:
                    time.sleep(sec)
                else:
                    raise

        try:
            yield ws
        finally:
            ws.close()

    with test_app.create_app() as app:
        with app.test_client():
            with app.app_context():
                import models # pylint: disable=import-outside-toplevel
                models.init_schema(app.config['DSN'])

                with serve_wss(app):
                    yield connect

def test_chat(): # pylint: disable=missing-function-docstring
    with get_connect_fn() as connect:
        with connect() as ws: # pylint: disable=invalid-name
            timestamp = str(time.time())
            ws.send(json.dumps(dict(type=web.chat.EVENT_ECHO, message=timestamp)))
            resp = ws.recv()
            assert timestamp == resp, resp
