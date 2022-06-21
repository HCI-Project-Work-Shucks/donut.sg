# pylint: disable=missing-module-docstring
import sqlalchemy
import sqlalchemy.orm
from sqlalchemy.ext import declarative

Base = declarative.declarative_base()

engine = None  # pylint: disable=invalid-name
session = None  # pylint: disable=invalid-name


def get(cls, pk):  # pylint: disable=invalid-name
    '''Gets the cls instance by PK.'''
    return session.query(cls).get(pk)


def query(cls, *criteria):
    '''Queries and maps to the cls instances.'''
    return session.query(cls).filter(*criteria).all()


def insert(obj):  # pylint: disable=missing-function-docstring
    session.add(obj)
    session.commit()
    session.refresh(obj)


def delete(obj):
    session.delete(obj)
    session.commit()


def set_defaults(eng, sess):
    '''Sets the global engine and session.'''
    global engine, session  # pylint: disable=invalid-name,global-statement
    engine = eng
    session = sess
    Base.query = session.query_property()


def create_engine(dsn):  # pylint: disable=missing-function-docstring
    eng = sqlalchemy.create_engine(dsn, echo=True)
    sess = sqlalchemy.orm.scoped_session(sqlalchemy.orm.sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=eng,
    ))
    return eng, sess
