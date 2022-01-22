# pylint: disable=missing-module-docstring
import http
import traceback

import flask

from web import errors

def respond_ok(message):
    '''200 response'''
    return flask.make_response(message, http.HTTPStatus.OK)

def respond_not_found(message):
    '''404 response'''
    return flask.make_response(message, http.HTTPStatus.NOT_FOUND)

def respond_bad_request(code, message):
    '''400 response'''
    return flask.jsonify(errors.BadRequest(code, message))

def respond_exception():
    '''Responds a 500 with exception's traceback.'''
    return flask.make_response(traceback.format_exc(), http.HTTPStatus.INTERNAL_SERVER_ERROR)
