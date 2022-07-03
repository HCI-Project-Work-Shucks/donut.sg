import flask

import exceptions
import web
from models import donations
import fulfilments

bp = flask.Blueprint('donations', __name__)

@bp.route('/<int:ident>', methods=('PUT',))
def update():
    data = flask.request.get_json()
    owner = data.get('owner')
    desc = data.get('desc')
    closed = data.get('closed')
    deleted = data.get('deleted')

    try:
        if closed == True:
            user = donations.Donation.change(owner, desc, closed, deleted)
            fulfilments.update(owner)
        else:
            user = donations.Donation.change(owner, desc, deleted)
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
        donation = donations.Donation.create(owner, title, desc, closed, deleted, time, picture)
    except Exception:
        return web.respond_exception()

    return flask.jsonify(donation.to_dict())
