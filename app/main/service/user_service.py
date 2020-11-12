from app.main.resource.errors import UnauthorizedError
import datetime
from functools import wraps
from flask import jsonify, abort
from flask.globals import request

from app.main import db
from app.main.model.user_model import UserModel
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_jwt_extended.view_decorators import _decode_jwt_from_request
from flask_jwt_extended.exceptions import NoAuthorizationError
from flask_jwt_extended import decode_token


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


def check_token(email, token):
    if(UserModel.query.filter_by(email=email, access_token=token).first()):
        return True
    else:
        return False


def save_changes(data):
    db.session.add(data)
    db.session.commit()

def set_token(email, token):
    user = get_a_user_by_email(email)
    user.access_token = token
    db.session.add(user)
    db.session.commit()


def custom_jwt_required(view_function):
    @wraps(view_function)
    def wrapper(*args, **kwargs):
        try:
            jwt_data = decode_token(request.headers['token'])
        except Exception:
            jwt_data = None

        print(jwt_data)

        if jwt_data and ('identity' in jwt_data):
            if check_token(jwt_data['identity'], request.headers['token'] or None) and datetime.datetime.now().timestamp() < jwt_data['exp']:
                authorized = True
            else:
                authorized = False
        else:
            authorized = False

        if not authorized:
            raise UnauthorizedError

        return view_function(*args, **kwargs)

    return wrapper
