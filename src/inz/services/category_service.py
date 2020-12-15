from inz.models.category import Category
from inz import db
from inz.exceptions.unauthorized_error import UnauthorizedError
from inz.exceptions.record_not_found_error import RecordNotFoundError
from inz.utility.duration_utility import duration_contains
from datetime import date


class CategoryService:
    @staticmethod
    def create(name, user_id):
        new_category = Category(name=name, user_id=user_id)
        db.session.add(new_category)
        db.session.commit()
        return new_category

    @staticmethod
    def update(category_id, current_user_id, name):
        # validate access
        CategoryService.get_by_id(category_id, current_user_id)

        if name is None:
            return

        # name is only changable property, user_id field cannot be changed
        Category.query.filter_by(id=category_id).update(dict(name=name))
        db.session.commit()

    @ staticmethod
    def delete(category_id, current_user_id):
        category = CategoryService.get_by_id(category_id, current_user_id)
        db.session.delete(category)
        db.session.commit()

    @ staticmethod
    def get_by_id(category_id, current_user_id):
        category = Category.query.get(category_id)
        if category is None:
            raise RecordNotFoundError()
        if category.user_id != current_user_id:
            raise UnauthorizedError()
        return category

    @staticmethod
    def get_category_analysis(start_date_string, end_date_string,
                              current_user_categories,
                              current_user_expenses):
        start = date.fromisoformat(start_date_string)
        end = date.fromisoformat(end_date_string)

        total_spending = sum(
            [expense.price * expense.amount
             for expense in current_user_expenses
             if duration_contains(start, end, expense.date)])

        spending_per_category = {
            category.name: sum(
                [expense.price * expense.amount
                 for expense in category.expenses
                 if duration_contains(start, end, expense.date)])
            for category in current_user_categories}

        spending_per_category['no category'] = total_spending - sum(
            [category_spending
             for category_spending in spending_per_category.values()])

        if(total_spending == 0):
            return {'total_spending': 0, 'categories': [{'category_name': category_name, 
                    'spent_amount': 0, 'spent_percent': 0}
                      for category_name in spending_per_category.keys()]}

        analysis = {'total_spending': total_spending,
                    'categories': [
                        {'category_name': category_name,
                         'spent_amount': spending_per_category[category_name],
                         'spent_percent': round(
                             spending_per_category[category_name] * 100
                             / total_spending, 2)
                         }
                        for category_name in spending_per_category.keys()
                    ]}
        return analysis
