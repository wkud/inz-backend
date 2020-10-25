from flask import request
from flask_restful import Resource
from flask_api import status
from flask_jwt import jwt_required, current_identity
from inz import api
from inz.services.limit_service import LimitService
from inz.exceptions.unauthorized_error import UnauthorizedError
from inz.exceptions.record_not_found_error import RecordNotFoundError
from inz.exceptions.invalid_duration_error import InvalidDurationError


class LimitEndpoint(Resource):
    decorators = [jwt_required()]
    # http://127.0.0.1:5000/limit

    def post(self):
        data = request.get_json()
        try:
            new_limit = LimitService.create(data.get('duration_start'),
                                            data.get('duration_end'),
                                            data.get('planned_amount'),
                                            data.get('category_id'),
                                            current_identity.categories)
            return {'id': new_limit.id}
        except InvalidDurationError as err:
            return err.message, status.HTTP_406_NOT_ACCEPTABLE

    def get(self):
        return [limit.to_json()
                for category in current_identity.categories
                for limit in category.limits]


class LimitIdEndpoint(Resource):
    # http://127.0.0.1:5000/limit/{id}
    decorators = [jwt_required()]

    def get(self, id):
        try:
            limit = LimitService.get_by_id(id, current_identity.id)
            return limit.to_json()
        except RecordNotFoundError as err:
            return err.message, status.HTTP_404_NOT_FOUND
        except UnauthorizedError as err:
            return err.message, status.HTTP_401_UNAUTHORIZED

    def put(self, id):
        data = request.get_json()  # TODO to test if unathorized error needed
        try:
            LimitService.update(id, current_identity.id,
                                data.get('duration_start'),
                                data.get('duration_end'),
                                data.get('planned_amount'),
                                data.get('category_id'))
            return '', status.HTTP_204_NO_CONTENT
        except RecordNotFoundError as err:
            return err.message, status.HTTP_404_NOT_FOUND
        except UnauthorizedError as err:
            return err.message, status.HTTP_401_UNAUTHORIZED
        except InvalidDurationError as err:
            return err.message, status.HTTP_406_NOT_ACCEPTABLE

    def delete(self, id):
        try:
            LimitService.delete(id, current_identity.id)
            return '', status.HTTP_204_NO_CONTENT
        except RecordNotFoundError as err:
            return err.message, status.HTTP_404_NOT_FOUND
        except UnauthorizedError as err:
            return err.message, status.HTTP_401_UNAUTHORIZED


api.add_resource(LimitEndpoint, '/limit')
api.add_resource(LimitIdEndpoint, '/limit/<int:id>')
