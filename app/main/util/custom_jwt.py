from app.main.model.candidate_model import CandidateModel
from app.main.model.recruiter_model import RecruiterModel
from flask_restx.inputs import email
from app.main.util.response import response_object
from functools import wraps
from flask_jwt_extended import jwt_required
from flask_jwt_extended.utils import get_jwt_identity
from flask import jsonify

def HR_only(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        identity = get_jwt_identity()
        email = identity['email']
        is_HR = identity['is_HR']

        if not is_HR:
            return response_object(code=403, message="Bạn không có quyền thực hiện chức năng này!"), 403
        else:
            hr = RecruiterModel.query.filter_by(email=email).first()

            if not hr:
                return response_object(code=403, message="Bạn không có quyền thực hiện chức năng này!"), 403
            else:
                return func(*args, **kwargs)
        
    return jwt_required(wrapper)
    

def Candidate_only(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        identity = get_jwt_identity()
        email = identity['email']
        is_HR = identity['is_HR']

        # must
        if is_HR == True:
            return response_object(code=403, message="Bạn không có quyền thực hiện chức năng này!"), 403
        else:
            candidate = CandidateModel.query.filter_by(email=email).first()

            if not candidate:
                return response_object(code=403, message="Bạn không có quyền thực hiện chức năng này!"), 403
            else:
                return func(*args, **kwargs)
        
    return jwt_required(wrapper)