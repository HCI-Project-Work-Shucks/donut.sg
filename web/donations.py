import flask

import exceptions
import web
from models import donations
<<<<<<< HEAD
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
=======

bp = flask.Blueprint('donations', __name__)

>>>>>>> 0e2b709f7ab3c16c1a6580d6eccc2f2c72fe74ce

@bp.route('/', methods=('POST',))
def create():
    data = flask.request.get_json()
    owner = data.get("owner")
<<<<<<< HEAD
    title = data.get("title")
    desc = data.get("desc")
    closed = data.get("closed")
    deleted = data.get("deleted")
    time = data.get("time")
    picture = data.get("picture")

    try:
        donation = donations.Donation.create(owner, title, desc, closed, deleted, time, picture)
=======
    category = data.get("category")
    title = data.get("title")
    quantity = data.get("quantity")
    desc = data.get("desc")

    try:
        donation = donations.Donation.create(owner, category, title, quantity, desc)
>>>>>>> 0e2b709f7ab3c16c1a6580d6eccc2f2c72fe74ce
    except Exception:
        return web.respond_exception()

    return flask.jsonify(donation.to_dict())
