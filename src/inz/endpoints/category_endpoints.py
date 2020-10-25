from flask import request
from flask_restful import Resource
from flask_api import status
from flask_jwt import jwt_required, current_identity
from inz import api
from inz.services.category_service import CategoryService
from inz.exceptions.unauthorized_error import UnauthorizedError
from inz.exceptions.record_not_found_error import RecordNotFoundError


class CategoryEndpoint(Resource):
    decorators = [jwt_required()]
    # http://127.0.0.1:5000/category

    def post(self):
        data = request.get_json()
        new_category = CategoryService.create(data.get('name'),
                                              current_identity.id)
        return {'id': new_category.id}

    def get(self):
        all_user_categories = current_identity.categories
        return [category.to_json() for category in all_user_categories]


class CategoryIdEndpoint(Resource):
    # http://127.0.0.1:5000/category/{id}
    decorators = [jwt_required()]

    def get(self, id):
        try:
            category = CategoryService.get_by_id(id, current_identity.id)
            return category.to_json()
        except RecordNotFoundError as err:
            return err.message, status.HTTP_404_NOT_FOUND
        except UnauthorizedError as err:
            return err.message, status.HTTP_401_UNAUTHORIZED

    def put(self, id):
        data = request.get_json()  # TODO to test if unathorized error needed
        try:
            CategoryService.update(id, current_identity.id, data.get('name'))
            return '', status.HTTP_204_NO_CONTENT
        except RecordNotFoundError as err:
            return err.message, status.HTTP_404_NOT_FOUND
        except UnauthorizedError as err:
            return err.message, status.HTTP_401_UNAUTHORIZED

    def delete(self, id):
        try:
            CategoryService.delete(id, current_identity.id)
            return '', status.HTTP_204_NO_CONTENT
        except RecordNotFoundError as err:
            return err.message, status.HTTP_404_NOT_FOUND
        except UnauthorizedError as err:
            return err.message, status.HTTP_401_UNAUTHORIZED


api.add_resource(CategoryEndpoint, '/category')
api.add_resource(CategoryIdEndpoint, '/category/<int:id>')
