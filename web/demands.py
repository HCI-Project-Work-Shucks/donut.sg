import flask

import exceptions
import web
from models import demands

bp = flask.Blueprint('demands', __name__)


@bp.route('/', methods=('POST',))
def create():
    data = flask.request.get_json()
    category = int(data.get("category"))
    title = data.get("title")
    quantity = int(data.get("quantity"))
    desc = data.get("desc")

    try:
        demand = demands.Demand.create(category, title, quantity, desc)
    except Exception:
        return web.respond_exception()

    return flask.jsonify(demand.to_dict())
