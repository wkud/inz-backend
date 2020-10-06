from inz import db, app
from inz.models.user import User
from inz.services.user_auth_service import PasswordUtility
from flask_jwt import JWT
from werkzeug.security import safe_str_cmp


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

    @staticmethod
    def validate_credentials(email, password):
        user = UserService.get_by_email(email)
        if user is None:
            return False
        correct = PasswordUtility.check_password(user.password, password)
        return correct


# TODO try add JWT Utility static class here and redirect jwt ctor to JWTUtility.authenticate and .identify

class User1(object):
    def __init__(self, id, email, password):
        self.id = id
        self.email = email
        self.password = password

    def __str__(self):
        return "User(id='%s')" % self.id

users = [
    User1(1, 'user1', 'abcxyz'),
    User1(2, 'user2', 'abcxyz'),
]

email_table = {u.email: u for u in users}
userid_table = {u.id: u for u in users}


def authenticate(email, password):
    user = email_table.get(email, None)
    if user and safe_str_cmp(
            user.password.encode('utf-8'),
            password.encode('utf-8')):
        return user


def identity(payload):
    user_id = payload['identity']
    return userid_table.get(user_id, None)


app.config['SECRET_KEY'] = 'super-secret'
app.config['JWT_AUTH_URL_RULE'] = '/login'
app.config['JWT_AUTH_USERNAME_KEY'] = 'email'
jwt = JWT(app, authenticate, identity)
