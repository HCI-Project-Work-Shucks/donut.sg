# pylint: disable=missing-module-docstring
import http

from test_app import * # pylint: disable=wildcard-import,import-error
from web import auth

def test_login(client): # pylint: disable=missing-function-docstring
    email = 'a@g.mail'
    pwd = 'password'
    resp = client.post('/api/v1/users/', json=dict(email=email, password=pwd))
    assert http.HTTPStatus.OK == resp.status_code
    user = resp.get_json()
    assert user['id']

    resp = client.post('/api/v1/login', json=dict(email=email, password=pwd))
    assert http.HTTPStatus.OK == resp.status_code
    assert 'OK' == resp.data.decode('utf-8')
    assert auth.TOKEN_KEY in resp.headers

def test_logout(client): # pylint: disable=missing-function-docstring
    client.post('/api/v1/logout')
