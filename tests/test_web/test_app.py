# pylint: disable=missing-module-docstring
import http
import pathlib
import os
import shutil
import sys
import tempfile
import traceback

import pytest

sys.path.insert(0, pathlib.Path(__file__).resolve().parent.parent.parent.as_posix())

@pytest.fixture
def client():
    '''a faked client of HTTP request'''
    db_dir = tempfile.mkdtemp()
    dsn = os.path.join('sqlite:////', db_dir.strip('/'), 'unitest.sqlite')

    from web import wsgi # pylint: disable=import-outside-toplevel
    app = wsgi.create_app(dict(TESTING=True, DSN=dsn))

    with app.test_client() as cli:
        with app.app_context():
            import models # pylint: disable=import-outside-toplevel
            models.init_schema(app.config['DSN'])

        try:
            yield cli
        except Exception: # pylint: disable=broad-except
            traceback.print_exc()
        finally:
            shutil.rmtree(db_dir)

def test_ping(client): # pylint: disable=missing-function-docstring,redefined-outer-name
    resp = client.get('/ping')
    assert http.HTTPStatus.OK == resp.status_code
    assert 'pong' == resp.data.decode('utf-8')
