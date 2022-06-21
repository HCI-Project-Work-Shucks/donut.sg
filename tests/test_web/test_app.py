# pylint: disable=missing-module-docstring
import contextlib
import http
import pathlib
import os
import shutil
import sys
import tempfile

import pytest

sys.path.insert(0, pathlib.Path(__file__).resolve().parent.parent.parent.as_posix())


@contextlib.contextmanager
def create_app():  # pylint: disable=missing-function-docstring
    db_dir = tempfile.mkdtemp()
    dsn = "sqlite:///" + os.path.join(db_dir.strip('/'), "unitest.sqlite")

    from web import wsgi  # pylint: disable=import-outside-toplevel
    app = wsgi.create_app(dict(TESTING=True, DSN=dsn))

    with app.app_context():
        import models  # pylint: disable=import-outside-toplevel
        models.init_schema(app.config['DSN'])

    try:
        yield app
    finally:
        shutil.rmtree(db_dir)


@pytest.fixture
def client():
    '''a faked client of HTTP request'''
    with create_app() as app:
        with app.test_client() as cli:
            yield cli


def test_ping(client):  # pylint: disable=missing-function-docstring,redefined-outer-name
    resp = client.get('/ping')
    assert http.HTTPStatus.OK == resp.status_code
    assert 'pong' == resp.data.decode('utf-8')
