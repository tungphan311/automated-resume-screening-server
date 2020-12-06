from app.main.model.candidate_model import CandidateModel
from app.main.util.dto import CandidateDto
from werkzeug.exceptions import ExpectationFailed
from app.main.resource.errors import UnauthorizedError
import datetime
from functools import wraps
from flask import jsonify, abort
from flask.globals import request

from app.main import db
from app.main.model.account_model import AccountModel
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_jwt_extended.view_decorators import _decode_jwt_from_request
from flask_jwt_extended.exceptions import NoAuthorizationError
from flask_jwt_extended import decode_token
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)


def insert_new_account(account, candidate):
    account = AccountModel.query.filter_by(email=account['email']).first()
    if not account:
        new_account = AccountModel(
            email=account['email'],
            password=account['password'],
            phone = account['phone'],
            full_name = account['full_name'],
            gender = account['gender'],
            access_token=create_token(account['email'], 1),
            registered_on=datetime.datetime.utcnow()
        )
        candidate = CandidateModel(
            date_of_birth = candidate['date_of_birth'],
            account = new_account
        )
        db.session.add(new_account)
        db.session.add(candidate)
        db.session.commit()
        response_object = {
            'status': 'success',
            'message': 'Successfully registered.'
        }
        return response_object, 201
    else:
        response_object = {
            'status': 'fail',
            'message': 'account already exists. Please Log in.',
        }
        return response_object, 409

def delete_a_account_by_email(email):
    return AccountModel.query.filter_by(email=email).first()

def get_all_accounts():
    return AccountModel.query.all()


def get_a_account_by_email(email):
    return AccountModel.query.filter_by(email=email).first()


def get_a_account_by_sername(username):
    return AccountModel.query.filter_by(username=username).first()


def get_a_account_by_id(id):
    return AccountModel.query.filter_by(id=id).first()


def check_token(email, token):
    if(AccountModel.query.filter_by(email=email, access_token=token).first()):
        return True
    else:
        return False


def save_changes(data):
    db.session.add(data)
    db.session.commit()


def set_token(email, token):
    account = get_a_account_by_email(email)
    account.access_token = token
    db.session.add(account)
    db.session.commit()


def verify_account(email):
    account = get_a_account_by_email(email)
    account.confirmed = True
    account.confirmed_on = datetime.datetime.utcnow()
    db.session.add(account)
    db.session.commit()


def create_token(email, day=7):
    expires = datetime.timedelta(day)
    return create_access_token(email, expires_delta=expires)


# def custom_jwt_required(view_function):
#     @ wraps(view_function)
#     def wrapper(*args, **kwargs):
#         try:
#             jwt_data = decode_token(request.headers['token'])
#         except Exception:
#             jwt_data = None
#         # auth_header = request.headers.get('Authorization')

#         if jwt_data and ('identity' in jwt_data):
#             if check_token(jwt_data['identity'], request.headers['token'] or None) and datetime.datetime.now().timestamp() < jwt_data['exp']:
#                 authorized = True
#             else:
#                 authorized = False
#         else:
#             authorized = False

#         if not authorized:
#             raise UnauthorizedError

#         return view_function(*args, **kwargs)

#     return wrapper
