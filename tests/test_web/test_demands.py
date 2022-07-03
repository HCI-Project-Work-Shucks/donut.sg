import http

from test_app import *


def test_create_demand(client):
    owner = 1
    category = 1
    title = "my demand"
    quantity = 1
    desc = "i want a donut"
    resp = client.post("/api/v1/demands/", json=dict(owner=owner, category=category, title=title, quantity=quantity, desc=desc))
    assert http.HTTPStatus.OK == resp.status_code
    assert resp.get_json()["id"]
