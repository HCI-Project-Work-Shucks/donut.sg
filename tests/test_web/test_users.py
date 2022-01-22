# pylint: disable=missing-module-docstring
import http

from test_app import * # pylint: disable=wildcard-import,import-error

def test_register(client): # pylint: disable=missing-function-docstring
    resp = client.post('/api/v1/users/', json=dict(email='a@g.mail', password='password'))
    assert http.HTTPStatus.OK == resp.status_code
    user = resp.get_json()
    assert user['id']

    resp = client.get('/api/v1/users/'+str(user['id']))
    assert http.HTTPStatus.OK == resp.status_code
    assert user['id'] == resp.get_json()['id']
