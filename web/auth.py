# pylint: disable=missing-module-docstring
import functools
import http

import jwt
import flask

import exceptions
import web
from web import errors
from models import users

TOKEN_KEY = 'X-ACCESS-TOKENS'
SECRET_KEY = 'SECRET_KEY'
JWT_SIGNATURE_ALGORITHM = 'HS256'

bp = flask.Blueprint('auth', __name__)

@bp.before_app_request
def set_login_user_id():
    '''Loads the logged in user before any request.'''
    token = flask.request.headers.get(TOKEN_KEY)
    if not token:
        return

    payload = jwt.decode(token,
                         key=flask.current_app.config[SECRET_KEY],
                         algorithm=JWT_SIGNATURE_ALGORITHM)

    flask.g.login_user_id = payload.get('uid') # pylint: disable=assigning-non-slot

@bp.route('/login', methods=('POST',))
def login(): # pylint: disable=missing-function-docstring
    try:
        data = flask.request.get_json()
    except Exception: # pylint: disable=broad-except
        return web.respond_bad_request(*errors.CODE_INVALID_JSON)

    email = data.get('email')
    if email is None:
        return web.respond_bad_request(*errors.CODE_MISSING_EMAIL)

    try:
        user = users.User.get(email=data.get('email'))
    except exceptions.NotFoundError:
        return web.respond_bad_request(*errors.CODE_NO_SUCH_EMAIL)

    if not user.check_password(data.get('password')):
        return web.respond_bad_request(*errors.CODE_INCORRECT_PASSWORD)

    resp = web.respond_ok('OK')
    resp.headers[TOKEN_KEY] = jwt.encode(dict(id=user.id),
                                         key=flask.current_app.config[SECRET_KEY],
                                         algorithm=JWT_SIGNATURE_ALGORITHM)
    return resp

def login_required(view):
    '''A decorator for checking the request if is authorized.'''

    @functools.wraps(view)
    def wrapper(*args, **kwargs):
        try:
            uid = flask.g.login_user_id
        except AttributeError:
            return flask.make_response('unauthorized', http.HTTPStatus.UNAUTHORIZED)

        try:
            flask.g.login_user = users.User.get(uid) # pylint: disable=assigning-non-slot
        except exceptions.NotFoundError:
            return flask.make_response('forbidden', http.HTTPStatus.FORBIDDEN)
        except Exception: # pylint: disable=broad-except
            return web.respond_exception()

        return view(*args, **kwargs)

    return wrapper
