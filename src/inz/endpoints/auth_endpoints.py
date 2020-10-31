from flask import request
from flask_restful import Resource
from inz import api
from inz.services.user_service import UserService
from flask_jwt import jwt_required, current_identity

class RegisterEndpoint(Resource):
    # http://127.0.0.1:5000/register + credentials in json body
    # user credentials = email and password (not id)
    def post(self):
        user_data = request.get_json()
        email = user_data.get('email')
        password = user_data.get('password')
        new_user = UserService.create(email, password)
        return {'id': new_user.id}

# http://127.0.0.1:5000/login + credentials in body;
# this endpoint is provided by flask-jwt module


class IdentityEndpoint(Resource):
    # http://127.0.0.1:5000/protected
    decorators = [jwt_required()]

    def get(self):
        user = current_identity
        return {'id': user.id, 'email': user.email}


class TestEndpoint(Resource):
    # http://127.0.0.1:5000/test
    def get(self):
        return {'content': 'test complete'}


api.add_resource(RegisterEndpoint, '/register')
api.add_resource(IdentityEndpoint, '/identity')
api.add_resource(TestEndpoint, '/test')
