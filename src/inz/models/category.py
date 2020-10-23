from inz import db
from inz.models.expense import Expense  # noqa: F401


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)

    user_id = db.Column(
        db.Integer, db.ForeignKey('user.id'), nullable=False)
    # user - backref

    expenses = db.relationship('Expense', backref='ref_category', lazy=True)

    def __repr__(self):
        return f"Category({self.id}, '{self.name}', user: {self.user_id})"
