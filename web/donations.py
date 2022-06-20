import flask

import exceptions
import web
from models import donations

bp = flask.Blueprint('donations', __name__)


@bp.route('/', methods=('POST',))
def create():
    data = flask.request.get_json()
    category = int(data.get("category"))
    title = data.get("title")
    quantity = int(data.get("quantity"))
    desc = data.get("desc")

    try:
        donation = donations.Donation.create(category, title, quantity, desc)
    except Exception:
        return web.respond_exception()

    return flask.jsonify(donation.to_dict())
