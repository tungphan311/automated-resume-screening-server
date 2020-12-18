import datetime
from flask_jwt_extended import (create_access_token)
from app.main.config import Config as config

def create_token(email, is_HR = False, day=7):
    expires = datetime.timedelta(day)
    return create_access_token(identity={ 'email': email, 'is_HR': is_HR }, expires_delta=expires)

def get_url_verify_email(token,type):
    return config.BASE_URL_FE + "confirm-mail/?token="+ token+"&type="+type
