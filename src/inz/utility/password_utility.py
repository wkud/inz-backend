from inz import bcrypt


class PasswordUtility:
    @staticmethod
    def hash_password(password):
        password_utf8 = password.encode('utf-8')
        hashed = bcrypt.generate_password_hash(password_utf8).decode('utf-8')
        return hashed

    @staticmethod
    def check_password(correct_hashed_password, entered_password):
        correct = bcrypt.check_password_hash(
            correct_hashed_password, entered_password)
        return correct
