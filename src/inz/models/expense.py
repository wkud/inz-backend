from inz import db
from datetime import date


class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(20), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    date = db.Column(db.Date, default=date.today)

    user_id = db.Column(
        db.Integer, db.ForeignKey('user.id'), nullable=False)
    # user - backref

    category_id = db.Column(
        db.Integer, db.ForeignKey('category.id'), nullable=True)
    # category - backref

    def __repr__(self):
        return f"Expense({self.id}, '{self.product_name}', {self.price}, {self.amount}, \
        {self.date}, user: {self.user_id}, cat: {self.category_id})"

    def to_json(self):
        return {'id': self.id, 'product_name': self.product_name,
                'price': self.price, 'amount': self.amount,
                'date': self.date.isoformat(), 'user_id': self.user_id,
                'category_id': self.category_id,
                'category_name': self.category.name
                if self.category is not None else 'no category'}
