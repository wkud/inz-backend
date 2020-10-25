from inz.models.category import Category
from inz import db
from inz.exceptions.unauthorized_error import UnauthorizedError
from inz.exceptions.record_not_found_error import RecordNotFoundError


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
