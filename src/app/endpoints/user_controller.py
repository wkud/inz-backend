from flask import request
from flask_restful import Resource
from app import api
from app.services.user_repository import UserRepository


class UserEndpoint(Resource):
    # http://127.0.0.1:5000/users + data in json body
    # user data is: email and password (not id)
    def post(self):
        user_data = request.get_json()
        email = user_data.get('email')
        password = user_data.get('password')
        new_user = UserRepository.create(email, password)
        return {'id': new_user.id}


class UserEndpointId(Resource):
    # http://127.0.0.1:5000/users/id
    def get(self, id):
        user = UserRepository.get_by_id(id)
        return {'id': user.id, 'email': user.email}


api.add_resource(UserEndpoint, '/users')
api.add_resource(UserEndpointId, '/users/<int:id>')
