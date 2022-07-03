# pylint: disable=missing-module-docstring
import os
import pathlib
import sys

import flask
import flask_sockets

sys.path.insert(0, pathlib.Path(__file__).resolve().parent.parent.as_posix())
import db  # pylint: disable=wrong-import-position
from web import auth, chat, users, demands, donations, fulfilments  # pylint: disable=import-error, wrong-import-position


def create_app(test_config=None):
    '''Creates and configures an instance of the Flask application'''
    app = flask.Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        WSS_PORT=5001,
        DSN="sqlite:///" + os.path.join(app.instance_path.strip('/'), "donut.sqlite"),
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

    if app.config['SECRET_KEY'] == 'dev':
        db.Base.metadata.create_all(eng)

    @app.teardown_appcontext
    def shutdown_session(Exception=None):  # pylint: disable=unused-argument
        sess.remove()

    @app.route('/ping')
    def ping():
        return 'pong'

    app.register_blueprint(auth.bp, url_prefix='/api/v1')
    app.register_blueprint(users.bp, url_prefix='/api/v1/users')
    app.register_blueprint(demands.bp, url_prefix='/api/v1/demands')
    app.register_blueprint(donations.bp, url_prefix='/api/v1/donations')
    app.register_blueprint(fulfilments.bp, url_prefix='/api/v1/fulfilments')

    socks = flask_sockets.Sockets(app)
    socks.register_blueprint(chat.ws, url_prefix='/chats')

    return app
