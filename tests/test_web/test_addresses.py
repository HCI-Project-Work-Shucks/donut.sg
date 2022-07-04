import http

from test_app import *


def test_create_address(client):
    owner = 1
    title = "my address"
    desc = "my first address"
    postcode = "999999"
    resp = client.post("/api/v1/addresses/", json=dict(owner=owner, title=title, desc=desc, postcode=postcode))
    assert http.HTTPStatus.OK == resp.status_code
    assert resp.get_json()["id"]


def test_update_address(client):
    test_create_address(client)
    ident = 1
    new_title = "another address"
    new_desc = "my second address"
    new_postcode = "888888"
    resp = client.put(f"/api/v1/addresses/{ident}",
                                 json=dict(title=new_title, desc=new_desc, postcode=new_postcode))
    assert http.HTTPStatus.OK == resp.status_code
    assert resp.get_json()["id"]


def test_delete_address(client):
    test_create_address(client)
    ident = 1
    resp = client.delete(f"/api/v1/addresses/{ident}")
    assert http.HTTPStatus.OK == resp.status_code
    assert resp.get_json()["deleted"]
