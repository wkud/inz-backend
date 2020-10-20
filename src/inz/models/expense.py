from inz import db
from datetime import datetime


class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(20), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)  # convert to utc+1
    fk_user_id = db.Column(
        db.Integer, db.ForeignKey('user.id'), nullable=False)
    # fk_user - backref
    # fk_category_id

    def __repr__(self):
        return f"User({self.id}, '{self.product_name}', \
        {self.price}, {self.amount}, {self.date}, {self.fk_user_id})"
