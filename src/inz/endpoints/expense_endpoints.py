from flask import request
from flask_restful import Resource
from flask_api import status
from flask_jwt import jwt_required, current_identity
from inz import api
from inz.services.expense_service import ExpenseService
from inz.exceptions.unauthorized_error import UnauthorizedError
from inz.exceptions.record_not_found_error import RecordNotFoundError


class ExpenseEndpoint(Resource):
    decorators = [jwt_required()]
    # http://127.0.0.1:5000/expense

    def post(self):
        data = request.get_json()
        new_expense = ExpenseService.create(data.get('product_name'),
                                            data.get('price'),
                                            data.get('amount'),
                                            data.get('date'),
                                            current_identity.id,
                                            data.get('category_id'))
        return {'id': new_expense.id}

    def get(self):
        all_user_expenses = current_identity.expenses
        return [expense.to_json() for expense in all_user_expenses]


class ExpenseIdEndpoint(Resource):
    # http://127.0.0.1:5000/expense/{id}
    decorators = [jwt_required()]

    def get(self, id):
        try:
            expense = ExpenseService.get_by_id(id, current_identity.id)
            return expense.to_json()
        except RecordNotFoundError as err:
            return err.message, status.HTTP_404_NOT_FOUND
        except UnauthorizedError as err:
            return err.message, status.HTTP_401_UNAUTHORIZED

    def put(self, id):
        data = request.get_json()  # TODO to test if unathorized error needed
        try:
            ExpenseService.update(id, current_identity.id,
                                  data.get('product_name'), data.get('price'),
                                  data.get('amount'), data.get('date'),
                                  data.get('category_id'))
            return '', status.HTTP_204_NO_CONTENT
        except RecordNotFoundError as err:
            return err.message, status.HTTP_404_NOT_FOUND
        except UnauthorizedError as err:
            return err.message, status.HTTP_401_UNAUTHORIZED

    def delete(self, id):
        try:
            ExpenseService.delete(id, current_identity.id)
            return '', status.HTTP_204_NO_CONTENT
        except RecordNotFoundError as err:
            return err.message, status.HTTP_404_NOT_FOUND
        except UnauthorizedError as err:
            return err.message, status.HTTP_401_UNAUTHORIZED


api.add_resource(ExpenseEndpoint, '/expense')
api.add_resource(ExpenseIdEndpoint, '/expense/<int:id>')
