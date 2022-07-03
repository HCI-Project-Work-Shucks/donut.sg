import flask

import exceptions
import web
from models import demands
import fulfilments

bp = flask.Blueprint('demands', __name__)

@bp.route('/<int:ident>', methods=('PUT',))
def update():
    data = flask.request.get_json()
    owner = data.get('owner')
    desc = data.get('desc')
    closed = data.get('closed')
    deleted = data.get('deleted')
    
    try:
        if closed == True:
            user = demands.Donation.change(owner, desc, closed, deleted)
            fulfilments.update(owner)
        else:
            user = demands.Donation.change(owner, desc, deleted)
    except Exception:  # pylint: disable=broad-except
        return web.respond_exception()

    return flask.jsonify(user.to_dict())

@bp.route('/', methods=('POST',))
def create():
    data = flask.request.get_json()
    owner = data.get("owner")
    title = data.get("title")
    desc = data.get("desc")
    closed = data.get("closed")
    deleted = data.get("deleted")
    time = data.get("time")
    picture = data.get("picture")

    try:
        demand = demands.Demand.create(owner, title, desc, closed, deleted, time, picture)
    except Exception:
        return web.respond_exception()

    return flask.jsonify(demand.to_dict())
