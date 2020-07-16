from app import db
from app.models.user import User


class UserRepository:
    def create(email, password):
        new_user = User(email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        return new_user

    def get_by_id(id):
        user = User.query.filter_by(id=id).first()
        return user
