import datetime

from app.main import db
from app.main.model.user_model import UserModel


def insert_new_user(data):
    user = UserModel.query.filter_by(email=data['email']).first()
    if not user:
        new_user = UserModel(
            # public_id=str(uuid.uuid4()),
            email=data['email'],
            username=data['username'],
            password=data['password'],
            registered_on=datetime.datetime.utcnow()
        )
        save_changes(new_user)
        response_object = {
            'status': 'success',
            'message': 'Successfully registered.'
        }
        return response_object, 201
    else:
        response_object = {
            'status': 'fail',
            'message': 'User already exists. Please Log in.',
        }
        return response_object, 409


def get_all_users():
    return UserModel.query.all()


def get_a_user_by_email(email):
    return UserModel.query.filter_by(email=email).first()


def get_a_user_by_id(id):
    return UserModel.query.filter_by(id=id).first()


def save_changes(data):
    db.session.add(data)
    db.session.commit()
