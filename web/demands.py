import flask

import exceptions
import web
from models import demands

bp = flask.Blueprint('demands', __name__)


@bp.route('/', methods=('POST',))
def create():
    data = flask.request.get_json()
    owner = data.get("owner")
    category = data.get("category")
    title = data.get("title")
    quantity = data.get("quantity")
    desc = data.get("desc")

    try:
        demand = demands.Demand.create(owner, category, title, quantity, desc)
    except Exception:
        return web.respond_exception()

    return flask.jsonify(demand.to_dict())
