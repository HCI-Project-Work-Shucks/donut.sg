import http

from test_app import *


def test_create_fulfilment(client):
    target_type = "demand"
    target_id = 1
    creator = 1
    status = "pending"
    resp = client.post("/api/v1/fulfilments/", json=dict(target_type=target_type, target_id=target_id, creator=creator, status=status))
    assert http.HTTPStatus.OK == resp.status_code
    assert resp.get_json()["id"]


def test_update_fulfilment(client):
    test_create_fulfilment(client)
    ident = 1
    status = "completed"
    resp = client.put(f"/api/v1/fulfilments/{ident}", json=dict(status=status))
    assert http.HTTPStatus.OK == resp.status_code
    assert resp.get_json()["id"]
