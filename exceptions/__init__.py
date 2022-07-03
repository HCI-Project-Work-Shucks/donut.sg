# pylint: disable=missing-module-docstring


class BaseError(BaseException):
    '''The base class of other errors'''

    def __init__(self, message):
        self.message = message
        super().__init__()


class NotFoundError(BaseError):
    '''The error of no such object'''
