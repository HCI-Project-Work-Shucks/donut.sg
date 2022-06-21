import sqlalchemy

import db
import exceptions


class Donation(db.Base):
    """Represents a donation object"""
    __tablename__ = "donation"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    owner = sqlalchemy.Column(sqlalchemy.Integer)
    category = sqlalchemy.Column(sqlalchemy.Integer)
    title = sqlalchemy.Column(sqlalchemy.TEXT)
    quantity = sqlalchemy.Column(sqlalchemy.Integer)
    desc = sqlalchemy.Column(sqlalchemy.TEXT)

    def __repr__(self):
        return f"<Donation: {self.id!r}>"

    def __init__(self, ident=None):
        self.id = ident
        self.owner = None
        self.category = None
        self.title = None
        self.quantity = 0
        self.desc = None

    @classmethod
    def create(cls, owner, category, title, quantity, desc):
        """Creates a new donation"""
        donation = Donation()
        donation.owner = owner
        donation.category = category
        donation.title = title
        donation.quantity = quantity
        donation.desc = desc

        db.insert(donation)

        return donation

    @classmethod
    def get(cls, ident):
        """Gets a donation by ID"""
        donation = db.get(Donation, ident)
        if not donation:
            raise exceptions.NotFoundError(f"No such donation ID: {ident}")
        return donation

    def to_dict(self):
        return dict(id=self.id, owner=self.owner, category=self.category, title=self.title, quantity=self.quantity, desc=self.desc)
