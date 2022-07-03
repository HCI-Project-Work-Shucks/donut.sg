import http

from test_app import *


def test_create_donation(client):
    owner = 1
    category = 1
    title = "my donation"
    quantity = 1
    desc = "give me a donut"
    resp = client.post("/api/v1/donations/", json=dict(owner=owner, category=category, title=title, quantity=quantity, desc=desc))
    assert http.HTTPStatus.OK == resp.status_code
    assert resp.get_json()["id"]
