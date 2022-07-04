import flask

import exceptions
import web
from models import fulfilments

bp = flask.Blueprint('fulfilments', __name__)


@bp.route('/', methods=('POST',))
def create():
    data = flask.request.get_json()
    target_type = data.get("target_type")
    target_id = data.get("target_id")
    creator = data.get("creator")

    try:
        fulfilment = fulfilments.Fulfilment.create(target_type, target_id, creator, "pending")
    except Exception:
        return web.respond_exception()

    return flask.jsonify(fulfilment.to_dict())


@bp.route('/<int:ident>', methods=('PUT',))
def update(ident):
<<<<<<< HEAD
    try:
        fulfilment = fulfilments.Fulfilment.change(ident, "closed")
=======
    status = flask.request.get_json().get("status")
    try:
        fulfilment = fulfilments.Fulfilment.update(ident, status)
>>>>>>> 0e2b709f7ab3c16c1a6580d6eccc2f2c72fe74ce
    except exceptions.NotFoundError as ex:
        return web.respond_not_found(ex.message)
    except Exception:
        return web.respond_exception()
    else:
        return flask.jsonify(fulfilment.to_dict())
