import datetime
from flask_jwt_extended import (create_access_token)


def create_token(email, day=7):
    expires = datetime.timedelta(day)
    return create_access_token(email, expires_delta=expires)

