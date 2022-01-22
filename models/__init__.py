# pylint: disable=missing-module-docstring
import db

def init_schema(dsn): # pylint: disable=missing-function-docstring
    eng, _ = db.create_engine(dsn)
    import models.users # pylint: disable=unused-import,import-outside-toplevel
    db.Base.metadata.create_all(bind=eng)
