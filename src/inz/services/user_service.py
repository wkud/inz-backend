from inz import db
from inz.models.user import User
from inz.services.user_auth_service import PasswordUtility


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
