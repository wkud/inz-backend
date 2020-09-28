from flask import request
from flask_restful import Resource
from inz import api
from inz.services.user_service import UserService
from flask_api import status


class RegisterEndpoint(Resource):
    # http://127.0.0.1:5000/register + data in json body
    # user data is: email and password (not id)
    def post(self):
        user_data = request.get_json()
        email = user_data.get('email')
        password = user_data.get('password')
        new_user = UserService.create(email, password)
        return {'id': new_user.id}


class LoginEndpoint(Resource):
    # http://127.0.0.1:5000/login
    def post(self):
        user_data = request.get_json()
        email = user_data.get('email')
        password = user_data.get('password')
        valid = UserService.validate_credentials(email, password)
        if valid:
            return 'ok'
        else:
            return 'Invalid login credentials', status.HTTP_406_NOT_ACCEPTABLE


class NeedAuthorizationEndpoint(Resource):
    # http://127.0.0.1:5000/access/{id}
    def get(self, id):
        user = UserService.get_by_id(id)
        return {'id': user.id, 'email': user.email}


api.add_resource(RegisterEndpoint, '/register')
api.add_resource(LoginEndpoint, '/login')
api.add_resource(NeedAuthorizationEndpoint, '/access/<int:id>')
