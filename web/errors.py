# pylint: disable=missing-module-docstring
import exceptions


class Error(exceptions.BaseError): # pylint: disable=too-few-public-methods
    '''The base error class of web errors'''


class BadRequest(Error): # pylint: disable=too-few-public-methods
    '''Represents an error of bad request.'''

    def __init__(self, code, message):
        super().__init__(message)
        self.code = code


CODE_INVALID_JSON = (50000, 'invalid json')
CODE_MISSING_EMAIL = (50100, 'missing email')
CODE_NO_SUCH_EMAIL = (50101, 'no such email')
CODE_INCORRECT_PASSWORD = (50102, 'incorrect password')
CODE_NO_SUCH_USER = (50103, 'no such user')
