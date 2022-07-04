import sqlalchemy

import db
import exceptions


class Donation(db.Base):
    """Represents a donation object"""
    __tablename__ = "donation"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    owner = sqlalchemy.Column(sqlalchemy.Integer)
    title = sqlalchemy.Column(sqlalchemy.TEXT)
    desc = sqlalchemy.Column(sqlalchemy.TEXT)
    closed = sqlalchemy.Column(sqlalchemy.Boolean)
    deleted = sqlalchemy.Column(sqlalchemy.Boolean)
    time = sqlalchemy.Column(sqlalchemy.TEXT)
    picture = sqlalchemy.Column(sqlalchemy.TEXT)

    

    def __repr__(self):
        return f"<Donation: {self.id!r}>"

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
        """Creates a new donation"""
        donation = Donation()
        donation.owner = owner
        donation.title = title
        donation.desc = desc
        donation.closed = closed
        donation.deleted = deleted
        donation.time = time
        donation.picture = picture
        

        db.insert(donation)

        return donation

    @classmethod
    def change(cls, owner, closed=None, deleted=None, desc=None, title=None):
        user = Donation.query.filter_by(owner==owner).first()

        if desc:
            db.update("desc", user, desc)
            
        if closed:
            db.update("closed", user, closed)
            
        if deleted: 
            db.update("deleted", user, deleted)

    @classmethod
    def get(cls, ident):
        """Gets a donation by ID"""
        donation = db.get(Donation, ident)
        if not donation:
            raise exceptions.NotFoundError(f"No such donation ID: {ident}")
        return donation

    def to_dict(self):
        return dict(id=self.id, owner=self.owner, title=self.title, desc=self.desc, closed=self.closed, deleted=self.deleted)
