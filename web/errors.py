# pylint: disable=missing-module-docstring
import json

import exceptions


class Error(exceptions.BaseError): # pylint: disable=too-few-public-methods
    '''The base error class of web errors'''


class BadRequest(Error): # pylint: disable=too-few-public-methods
    '''Represents an error of bad request.'''

    def __init__(self, code, message):
        super().__init__(message)
        self.code = code

    def dumps(self):
        '''Dumps to a json str.'''
        return json.dumps(dict(code=self.code, message=self.message))


ERR_MISSING_EVENT_TYPE = BadRequest(50101, 'missing event type')


ERR_INVALID_JSON        = (50000, 'invalid json')
ERR_MISSING_EMAIL       = (50100, 'missing email')
ERR_MISSING_EVENT_TYPE  = (50101, 'missing event type')
ERR_NO_SUCH_EMAIL       = (50200, 'no such email')
ERR_NO_SUCH_USER        = (50201, 'no such user')
ERR_INCORRECT_PASSWORD  = (50300, 'incorrect password')
