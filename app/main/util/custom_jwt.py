from functools import wraps
from flask_jwt_extended import jwt_required
from flask_jwt_extended.utils import get_jwt_identity
from flask import jsonify

def HR_only(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        identity = get_jwt_identity()
        is_HR = identity['is_HR']

        if not is_HR:
            return {'massage': "Bạn không có quyền thực hiện chức năng này!"}, 403
        else:
            return func(*args, **kwargs)
        
    return jwt_required(wrapper)
    

def Candidate_only(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        identity = get_jwt_identity()
        is_HR = identity['is_HR']

        if is_HR:
            return {'massage': "Bạn không có quyền thực hiện chức năng này!"}, 403
        else:
            return func(*args, **kwargs)
        
    return jwt_required(wrapper)