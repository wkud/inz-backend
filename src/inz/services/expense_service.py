from inz.models.expense import Expense
from inz import db
from datetime import date
from inz.exceptions.unauthorized_error import UnauthorizedError
from inz.exceptions.record_not_found_error import RecordNotFoundError
from inz.utility.list_utility import contains


class ExpenseService:
    @staticmethod
    def create(product_name, price, amount, date_string, user_id, category_id,
               current_user_categories):
        # validate access to category_id
        category_accessible = contains(current_user_categories,
                                       lambda c: c.id == category_id)
        if not category_accessible:
            raise UnauthorizedError(msg='Given category cannot be accessed')

        date_obj = date.fromisoformat(date_string)
        new_expense = Expense(product_name=product_name,
                              price=price, amount=amount, date=date_obj,
                              user_id=user_id, category_id=category_id)
        db.session.add(new_expense)
        db.session.commit()
        return new_expense

    @staticmethod
    def update(expense_id, current_user_id, product_name, price, amount,
               date_string, category_id, current_user_categories):
        # validate access
        ExpenseService.get_by_id(expense_id, current_user_id)

        # validate access to category_id
        category_accessible = contains(current_user_categories,
                                       lambda c: c.id == category_id)
        if not category_accessible:
            raise UnauthorizedError(msg='Given category cannot be accessed')

        # user_id field cannot be changed
        new_data = dict(product_name=product_name,
                        price=price, amount=amount, date=date_string,
                        category_id=category_id)
        for field in new_data.copy():
            if new_data[field] is None:
                del new_data[field]

        if len(new_data) == 0:
            return

        # if date_string != None: convert to date objects
        if 'date' in new_data:
            new_data['date'] = date.fromisoformat(date_string)

        Expense.query.filter_by(id=expense_id).update(new_data)
        db.session.commit()

    @ staticmethod
    def delete(expense_id, current_user_id):
        expense = ExpenseService.get_by_id(expense_id, current_user_id)
        db.session.delete(expense)
        db.session.commit()

    @ staticmethod
    def get_by_id(expense_id, current_user_id):
        expense = Expense.query.get(expense_id)
        if expense is None:
            raise RecordNotFoundError()
        if expense.user_id != current_user_id:
            raise UnauthorizedError()
        return expense
