import sqlalchemy

import db
import exceptions


class Address(db.Base):
    """Represents an address object"""
    __tablename__ = "address"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    owner = sqlalchemy.Column(sqlalchemy.Integer)
    title = sqlalchemy.Column(sqlalchemy.TEXT)
    desc = sqlalchemy.Column(sqlalchemy.TEXT)
    postcode = sqlalchemy.Column(sqlalchemy.VARCHAR(6))

    def __repr__(self):
        return f"<Address: {self.id!r}>"

    def __init__(self, ident=None):
        self.id = ident
        self.owner = None
        self.title = None
        self.desc = None
        self.postcode = None

    @classmethod
    def create(cls, owner, title, desc, postcode):
        """Creates a new address"""
        address = Address()
        address.owner = owner
        address.title = title
        address.desc = desc
        address.postcode = postcode

        db.insert(address)

        return address

    @classmethod
    def update(cls, ident, title, desc, postcode):
        """Update an address by ID"""
        address = Address.get(ident)
        address.title = title
        address.desc = desc
        address.postcode = postcode

        db.insert(address)

        return address

    @classmethod
    def delete(cls, ident):
        """Deletes an address by ID"""
        address = Address.get(ident)
        db.delete(address)
        return dict(id=ident, object="address", deleted=True)

    @classmethod
    def get(cls, ident):
        """Retrieves an address by ID"""
        address = db.get(Address, ident)
        if not address:
            raise exceptions.NotFoundError(f"No such address ID: {ident}")
        return address

    @classmethod
    def get_by_user(cls, owner):
        """Gets a list of address by the user ID"""
        addresses = db.query(Address, Address.owner == owner)
        return addresses

    def to_dict(self):
        return dict(id=self.id, owner=self.owner, title=self.title, desc=self.desc, postcode=self.postcode)
