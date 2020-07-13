from flask import Flask, request
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from config import ProductionConfig

# config
app = Flask('inz')
app.config.from_object(ProductionConfig())

api = Api(app)
db = SQLAlchemy(app)


# database
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"User({self.id}, '{self.email}')"


# test endpoints
class CreateUser(Resource):
    # http://127.0.0.1:5000/users + data in json body
    # user data is: email and password (not id)
    def post(self):
        user_data = request.get_json()
        email = user_data.get('email')
        password = user_data.get('password')
        new_user = User(email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        return {'id': new_user.id}


class GetUser(Resource):
    # http://127.0.0.1:5000/users/id
    def get(self, id):
        user = User.query.filter_by(id=id).first()
        return {'id': user.id, 'email': user.email}


api.add_resource(CreateUser, '/users')
api.add_resource(GetUser, '/users/<int:id>')


if __name__ == '__main__':
    app.run(debug=True)
