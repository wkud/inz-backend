from inz import db
from inz.models.user import User
from inz.models.expense import Expense
from inz.models.category import Category
from inz.models.limit import Limit
from datetime import datetime, date


def new_user(email, password='pass'):
    return User(email, password)


def new_cat(name, user_id=1):
    return Category(name=name, user_id=user_id)


def new_exp(product_name, price=1, amount=1, date=datetime.utcnow(),
            user_id=1, category_id=1):
    return Expense(product_name=product_name, price=price, amount=amount,
                   date=date, user_id=user_id, category_id=category_id)


def new_limit(duration_start=date.today(), duration_end=date.today(),
              planned_amount=100, category_id=1):
    return Limit(duration_start=duration_start, duration_end=duration_end,
                 planned_amount=planned_amount, category_id=category_id)


def commit(model):
    db.session.add(model)
    db.session.commit()
