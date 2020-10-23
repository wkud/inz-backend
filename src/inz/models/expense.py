from inz import db
from datetime import datetime


class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(20), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)  # convert to utc+1

    user_id = db.Column(
        db.Integer, db.ForeignKey('user.id'), nullable=False)
    # user - backref

    category_id = db.Column(
        db.Integer, db.ForeignKey('category.id'), nullable=False)
    # category - backref

    def __repr__(self):
        return f"Expense({self.id}, '{self.product_name}', {self.price}, {self.amount}, \
        {self.date}, user: {self.user_id}, cat: {self.category_id})"
