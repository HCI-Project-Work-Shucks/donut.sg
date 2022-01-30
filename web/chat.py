# pylint: disable=missing-module-docstring
import json

import flask

from web import errors

ws = flask.Blueprint('ws', __name__)

TYPE_KEY = 'type'
MESSAGE_KEY = 'message'

def echo(socket, event):
    '''The echo event handler.'''
    socket.send(event.get(MESSAGE_KEY))

EVENT_ECHO = 'echo'

handlers = {
    EVENT_ECHO: echo,
}

@ws.route('/')
def dispatch(socket):
    '''The ws events' dispatcher.'''
    gen_err_payload = lambda *a: dict(zip(('code', 'message'), a))

    while not socket.closed:
        raw = socket.receive()

        try:
            event = json.loads(raw)
        except json.decoder.JSONDecodeError:
            payload = gen_err_payload(*errors.ERR_INVALID_JSON)
            socket.send(json.dumps(payload))
            continue

        handle = handlers.get(event.get(TYPE_KEY))
        if not handle:
            payload = gen_err_payload(*errors.ERR_MISSING_EVENT_TYPE)
            socket.send(json.dumps(payload))
            continue

        handle(socket, event)
