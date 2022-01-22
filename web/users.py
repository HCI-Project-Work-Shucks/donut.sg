# pylint: disable=missing-module-docstring
import flask

import exceptions
import web
from models import users

bp = flask.Blueprint('users', __name__)

def check(email, pwd):
    '''Checks the validation of email address and plain text password for register.'''
    if not users.User.check_email(email):
        return ValueError('email')

    if not users.User.check_plain_password(pwd):
        return ValueError('pwd')

    return None

@bp.route('/<int:ident>', methods=('GET',))
def get(ident): # pylint: disable=missing-function-docstring
    try:
        user = users.User.get(ident=ident)
    except exceptions.NotFoundError as ex:
        return web.respond_not_found(ex.message)
    except Exception: # pylint: disable=broad-except
        return web.respond_exception()
    else:
        return flask.jsonify(user.to_dict())

@bp.route('/', methods=('POST',))
def register(): # pylint: disable=missing-function-docstring
    data = flask.request.get_json()
    email = data.get('email')
    pwd = data.get('password')
    err = check(email, pwd)
    if err is not None:
        return flask.jsonify(err)

    try:
        user = users.User.create(email, pwd)
    except Exception: # pylint: disable=broad-except
        return web.respond_exception()

    return flask.jsonify(user.to_dict())
