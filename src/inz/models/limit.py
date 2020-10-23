from inz import db
from datetime import date


class Limit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    duration_start = db.Column(db.Date, default=date.today)
    duration_end = db.Column(db.Date, default=date.today)
    planned_amount = db.Column(db.Integer, nullable=False)

    category_id = db.Column(
        db.Integer, db.ForeignKey('category.id'), nullable=False)
    # category - backref

    def __repr__(self):
        return f"Limit({self.id}, {self.duration_start}, {self.duration_end}, \
        {self.planned_amount}, cat: {self.category_id})"
