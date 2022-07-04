# pylint: disable=missing-module-docstring
import flask

import exceptions
import web
<<<<<<< HEAD
from models import users
=======
from models import users, addresses
>>>>>>> 0e2b709f7ab3c16c1a6580d6eccc2f2c72fe74ce

bp = flask.Blueprint('users', __name__)


def check(email, pwd):
    '''Checks the validation of email address and plain text password for register.'''
    if not users.User.check_email(email):
        return ValueError('email')

    if not users.User.check_plain_password(pwd):
        return ValueError('pwd')

    return None


<<<<<<< HEAD
@bp.route('/<int:ident>', methods=('PUT',))
def change(ident):
    data = flask.request.get_json()
    email = data.get('email')
    about = data.get('about')
    profile_pic = data.get('profilePic')
    completed_deals = data.get('completedDeals')
    pending_deals = data.get('pendingDeals')

    try:
        user = users.User.change(ident, completed_deals, pending_deals, about, profile_pic)
    except Exception:  # pylint: disable=broad-except
        return web.respond_exception()

    return flask.jsonify(user.to_dict())

=======
>>>>>>> 0e2b709f7ab3c16c1a6580d6eccc2f2c72fe74ce
@bp.route('/<int:ident>', methods=('GET',))
def get(ident):  # pylint: disable=missing-function-docstring
    try:
        user = users.User.get(ident=ident)
<<<<<<< HEAD
        return user
=======
>>>>>>> 0e2b709f7ab3c16c1a6580d6eccc2f2c72fe74ce
    except exceptions.NotFoundError as ex:
        return web.respond_not_found(ex.message)
    except Exception:  # pylint: disable=broad-except
        return web.respond_exception()
    else:
        return flask.jsonify(user.to_dict())

<<<<<<< HEAD
@bp.route('/', methods=('POST',))
def register():  # pylint: disable=missing-function-docstring
    data = flask.request.get_json()
    name = data.get('name')
    email = data.get('email')
    pwd = data.get('password')
    completed_deals = 0
    pending_deals = 0
    about = 'Hello I am a Donut'
    profile_pic = data.get('profilePic')

=======

@bp.route('/<int:ident>/addresses', methods=('GET',))
def get_addresses(ident):
    try:
        user_addresses = addresses.Address.get(ident)
    except Exception:
        return web.respond_exception()
    else:
        return {"object": "list", "has_more": False, "data": user_addresses}


@bp.route('/', methods=('POST',))
def register():  # pylint: disable=missing-function-docstring
    data = flask.request.get_json()
    email = data.get('email')
    pwd = data.get('password')
>>>>>>> 0e2b709f7ab3c16c1a6580d6eccc2f2c72fe74ce
    err = check(email, pwd)
    if err is not None:
        return flask.jsonify(err)

    try:
<<<<<<< HEAD
        user = users.User.create(email, pwd, name, completed_deals, pending_deals, about, profile_pic)
=======
        user = users.User.create(email, pwd)
>>>>>>> 0e2b709f7ab3c16c1a6580d6eccc2f2c72fe74ce
    except Exception:  # pylint: disable=broad-except
        return web.respond_exception()

    return flask.jsonify(user.to_dict())
