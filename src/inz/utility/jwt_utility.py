from inz.services.user_service import UserService
from inz.utility.password_utility import PasswordUtility


class JwtUtility:
    @staticmethod
    def authenticate(email, password):
        user = UserService.get_by_email(email)
        if user and PasswordUtility.check_password(user.password, password):
            return user

    @staticmethod
    def identity(payload):
        user_id = payload['identity']
        return UserService.get_by_id(user_id)
