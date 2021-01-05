from datetime import datetime
from app import db


class Payment(db.Model):
    __tablename__ = 'payment'

    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Numeric, index=True)
    currency = db.Column(db.String(5), index=True)
    description = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    shop_id = db.Column(db.Integer)
    shop_order_id = db.Column(db.String(255))

    def __init__(self, amount, currency, description, shop_id, shop_order_id):
        self.amount = amount
        self.currency = currency
        self.description = description
        self.shop_id = shop_id
        self.shop_order_id = shop_order_id

    def __repr__(self):
        return self.shop_order_id
