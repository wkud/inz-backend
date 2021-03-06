from inz import db
from inz.models.expense import Expense  # noqa: F401
from inz.models.category import Category  # noqa: F401


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    expenses = db.relationship('Expense', backref='user', lazy=True)
    categories = db.relationship('Category', backref='user', lazy=True)

    def __repr__(self):
        return f"User({self.id}, '{self.email}', '{self.password}')"
