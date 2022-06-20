import sqlalchemy

import db
import exceptions


class Fulfilment(db.Base):
    """Represents a fulfilment object"""
    __tablename__ = "fulfilment"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    target_type = sqlalchemy.Column(sqlalchemy.TEXT)
    target_id = sqlalchemy.Column(sqlalchemy.Integer)
    creator = sqlalchemy.Column(sqlalchemy.Integer)
    status = sqlalchemy.Column(sqlalchemy.TEXT)

    def __repr__(self):
        return f"<Fulfilment: {self.id!r}>"

    def __init__(self, ident=None):
        self.id = ident
        self.target_type = None
        self.target_id = None
        self.creator = None
        self.status = None

    @classmethod
    def create(cls, target_type, target_id, creator, status):
        """Creates a new fulfilment"""
        fulfilment = Fulfilment()
        fulfilment.target_type = target_type
        fulfilment.target_id = target_id
        fulfilment.creator = creator
        fulfilment.status = status

        db.insert(fulfilment)

        return fulfilment

    @classmethod
    def get(cls, ident):
        """Gets a fulfilment by ID"""
        fulfilment = db.get(Fulfilment, ident)
        if not fulfilment:
            raise exceptions.NotFoundError(f"No such fulfilment ID: {ident}")
        return fulfilment

    @classmethod
    def update(cls, ident, status):
        fulfilment = Fulfilment.get(ident)
        fulfilment.status = status
        db.insert(fulfilment)
        return fulfilment

    def to_dict(self):
        return dict(id=self.id, target_type=self.target_type, target_id=self.target_id, creator=self.creator,
                    status=self.status)
