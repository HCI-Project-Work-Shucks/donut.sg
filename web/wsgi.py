# pylint: disable=missing-module-docstring
import os
import pathlib
import sys

import flask

import db

sys.path.insert(0, pathlib.Path(__file__).resolve().parent.parent.as_posix())
from web import auth, users # pylint: disable=import-error, wrong-import-position

def create_app(test_config=None):
    '''Creates and configures an instance of the Flask application'''
    app = flask.Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DSN=os.path.join('sqlite:////', app.instance_path.strip('/'), 'donut.sqlite'),
    )

    if test_config:
        app.config.update(test_config)
    else:
        app.config.from_pyfile('config.py', silent=True)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    eng, sess = db.create_engine(app.config['DSN'])
    db.set_defaults(eng, sess)

    @app.teardown_appcontext
    def shutdown_session(exception=None): # pylint: disable=unused-argument
        sess.remove()

    @app.route('/ping')
    def ping():
        return 'pong'

    app.register_blueprint(auth.bp, url_prefix='/api/v1')
    app.register_blueprint(users.bp, url_prefix='/api/v1/users')

    return app
