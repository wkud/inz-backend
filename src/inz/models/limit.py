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

    def to_json(self):
        return {'id': self.id,
                'duration_start': date.isoformat(self.duration_start),
                'duration_end': date.isoformat(self.duration_end),
                'planned_amount': self.planned_amount,
                'category_id': self.category_id}
