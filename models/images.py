import sqlalchemy

import db
import exceptions


class Image(db.Base):
    """Represents an image object"""
    __tablename__ = "images"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    target_type = sqlalchemy.Column(sqlalchemy.TEXT)
    target_id = sqlalchemy.Column(sqlalchemy.Integer)
    url = sqlalchemy.Column(sqlalchemy.TEXT)

    def __repr__(self):
        return f"<Image: {self.id!r}>"

    def __init__(self, ident=None):
        self.id = ident
        self.target_type = None
        self.target_id = None
        self.url = url
