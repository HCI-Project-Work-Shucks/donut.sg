import sqlalchemy

import db
import exceptions


class Demand(db.Base):
    """Represents a demand object"""
    __tablename__ = "demand"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    owner = sqlalchemy.Column(sqlalchemy.Integer)
    category = sqlalchemy.Column(sqlalchemy.Integer)
    title = sqlalchemy.Column(sqlalchemy.TEXT)
    quantity = sqlalchemy.Column(sqlalchemy.Integer)
    desc = sqlalchemy.Column(sqlalchemy.TEXT)

    def __repr__(self):
        return f"<Demand: {self.id!r}>"

    def __init__(self, ident=None):
        self.id = ident
        self.owner = None
        self.category = None
        self.title = None
        self.quantity = 0
        self.desc = None

    @classmethod
    def create(cls, owner, category, title, quantity, desc):
        """Creates a new demand"""
        demand = Demand()
        demand.owner = owner
        demand.category = category
        demand.title = title
        demand.quantity = quantity
        demand.desc = desc

        db.insert(demand)

        return demand

    @classmethod
    def get(cls, ident):
        """Gets a demand by ID"""
        demand = db.get(Demand, ident)
        if not demand:
            raise exceptions.NotFoundError(f"No such demand ID: {ident}")
        return demand

    def to_dict(self):
        return dict(id=self.id, owner=self.owner, category=self.category, title=self.title, quantity=self.quantity, desc=self.desc)
