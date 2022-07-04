import sqlalchemy

import db
import exceptions

import users


class Fulfilment(db.Base):
    """Represents a fulfilment object"""
    __tablename__ = "fulfilment"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    target_name = sqlalchemy.Column(sqlalchemy.TEXT)
    target_id = sqlalchemy.Column(sqlalchemy.Integer)
    creator = sqlalchemy.Column(sqlalchemy.Integer)
    status = sqlalchemy.Column(sqlalchemy.TEXT)

    def __repr__(self):
        return f"<Fulfilment: {self.id!r}>"

    def __init__(self, ident=None):
        self.id = ident
        self.target_name = None
        self.target_id = None
        self.creator = None
        self.status = None

    @classmethod
    def create(cls, target_name, target_id, creator, status):
        """Creates a new fulfilment"""
        fulfilment = Fulfilment()
        fulfilment.target_name = target_name
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
    def change(cls, ident, status):
         deal = Fulfilment.query.filter_by(id==ident).first()
         db.update("status", deal, status)
         creator = users.User.query.filter_by(id==deal.creator).first()
         target = users.User.query.filter_by(id==deal.target).first()
         if status == 'closed': 
             creator_deal = creator.completedDeals + 1
             target_deal = target.completedDeals + 1
             users.change(deal.creator, completedDeals = creator_deal)
             users.change(deal.target, completedDeals = target_deal)
         elif status == 'pending':
             creator_deal = creator.pendingDeals + 1
             target_deal = target.pendingDeals + 1
             users.change(deal.creator, pendingDeals = creator_deal)
             users.change(deal.target, pendingDeals = target_deal)

        
    #     fulfilment = Fulfilment.get(ident)
    #     fulfilment.status = status
    #     db.insert(fulfilment)
    #     return fulfilment

    def to_dict(self):
        return dict(id=self.id, target_type=self.target_type, target_id=self.target_id, creator=self.creator,
                    status=self.status)
