import flask

import db
import exceptions
import web
from models import addresses

bp = flask.Blueprint('addresses', __name__)


@bp.route('/', methods=('POST',))
def create():
    data = flask.request.get_json()
    owner = data.get("owner")
    title = data.get("title")
    desc = data.get("desc")
    postcode = data.get("postcode")

    try:
        address = addresses.Address.create(owner, title, desc, postcode)
    except Exception:
        return web.respond_exception()

    return flask.jsonify(address.to_dict())


@bp.route('/<int:ident>', methods=('PUT',))
def update(ident):
    data = flask.request.get_json()
    title = data.get("title")
    desc = data.get("desc")
    postcode = data.get("postcode")

    try:
        address = addresses.Address.update(ident, title, desc, postcode)
    except exceptions.NotFoundError as ex:
        return web.respond_not_found(ex.message)
    except Exception:
        return web.respond_exception()
    else:
        return flask.jsonify(address.to_dict())


@bp.route('/<int:ident>', methods=('DELETE',))
def delete(ident):
    try:
        response = addresses.Address.delete(ident)
    except exceptions.NotFoundError as ex:
        return web.respond_not_found(ex.message)
    except Exception:
        return web.respond_exception()
    else:
        return flask.jsonify(response)
