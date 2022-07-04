from email.errors import CloseBoundaryNotFoundDefect
import sqlalchemy

import db
import exceptions


class Demand(db.Base):
    """Represents a demand object"""
    __tablename__ = "demand"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    owner = sqlalchemy.Column(sqlalchemy.Integer)
    title = sqlalchemy.Column(sqlalchemy.TEXT)
    desc = sqlalchemy.Column(sqlalchemy.TEXT)
    closed = sqlalchemy.Column(sqlalchemy.Boolean)
    deleted = sqlalchemy.Column(sqlalchemy.Boolean)
    time = sqlalchemy.Column(sqlalchemy.TEXT)
    picture = sqlalchemy.Column(sqlalchemy.TEXT)
    

    def __repr__(self):
        return f"<Demand: {self.id!r}>"

    def __init__(self, ident=None):
        self.id = ident
        self.owner = None
        self.title = None
        self.desc = None
        self.closed = False
        self.deleted = False
        self.time = None
        self.picture = None

    @classmethod
    def create(cls, owner, title, desc, closed, deleted, time, picture):
        """Creates a new demand"""
        demand = Demand()
        demand.owner = owner
        demand.title = title
        demand.desc = desc
        demand.closed = closed
        demand.deleted = deleted
        demand.time = time
        demand.picture = picture
        
        db.insert(demand)

        return demand
    @classmethod
    def change(cls, owner, closed=None, deleted=None, desc=None):
        user = Demand.query.filter_by(owner==owner).first()

        if desc:
            db.update("desc", user, desc)
            
        if closed:
            db.update("closed", user, closed)
            
        if deleted: 
            db.update("deleted", user, deleted)

    @classmethod
    def get(cls, ident):
        """Gets a demand by ID"""
        demand = db.get(Demand, ident)
        if not demand:
            raise exceptions.NotFoundError(f"No such demand ID: {ident}")
        return demand

    def to_dict(self):
        return dict(id=self.id, owner=self.owner, title=self.title, desc=self.desc, closed=self.closed, deleted=self.deleted)
