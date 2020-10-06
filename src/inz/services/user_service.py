from inz import db, app
from inz.models.user import User
from inz.utility.password_utility import PasswordUtility
from flask_jwt import JWT


class UserService:
    @staticmethod
    def create(email, password):
        hashed_password = PasswordUtility.hash_password(password)
        new_user = User(email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return new_user

    @staticmethod
    def get_by_id(id):
        user = User.query.get(id)
        return user

    @staticmethod
    def get_by_email(email):
        user = User.query.filter_by(email=email).first()
        return user


from inz.utility.jwt_utility import JwtUtility  # noqa: E402


jwt = JWT(app, JwtUtility.authenticate, JwtUtility.identity)
