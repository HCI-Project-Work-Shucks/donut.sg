# pylint: disable=missing-module-docstring
import re

import sqlalchemy
from werkzeug import security

import db
import exceptions


class User(db.Base):
    '''Represents a user object'''
    __tablename__ = 'user'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    email = sqlalchemy.Column(sqlalchemy.VARCHAR(512), unique=True)
    password = sqlalchemy.Column(sqlalchemy.CHAR(128))

    email_re = re.compile(r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$')

    def __repr__(self):
        return f'<User: {self.id!r}>'

    def __init__(self, ident=None):
        self.id = ident # pylint: disable=invalid-name
        self.password = None
        self.email = None

    def check_password(self, password):
        '''Checks the password (plain text) if is match to.'''
        return security.check_password_hash(self.password, password)

    @classmethod
    def create(cls, email, pwd):
        '''Creates a new user.'''
        user = User()
        user.email = email
        user.password = security.generate_password_hash(pwd)

        db.insert(user)

        return user

    @classmethod
    def get(cls, ident=None, email=None):
        '''Loads the user by ID or email.'''
        user = None

        if ident:
            user = db.get(User, ident)
            if not user:
                raise exceptions.NotFoundError(f'no such user id: {ident}')

        if email:
            users = db.query(User, User.email==email)
            if not users or len(users) != 1:
                raise exceptions.NotFoundError(f'no such email: {email}')

            user = users[0]

        return user

    @classmethod
    def check_plain_password(cls, pwd):
        '''Checks the validation of a plain text password.'''
        return 6 <= len(pwd) <= 16

    @classmethod
    def check_email(cls, email):
        '''Checks the validation of an email address.'''
        return cls.email_re.fullmatch(email)

    def to_dict(self): # pylint: disable=missing-function-docstring
        return dict(id=self.id,
                    email=self.email)
