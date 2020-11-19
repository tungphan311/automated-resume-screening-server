from datetime import datetime
from os import error

from flask import Blueprint
from flask.globals import request
from flask_mail import Message
from flask_restx import Api

from app.main.resource.errors import UnauthorizedError

from .main.controller.user_controller import UserList, UserVerify
from .main.controller.user_controller import api as user_ns

blueprint = Blueprint('api', __name__, url_prefix="/api", template_folder='templates')

api = Api(blueprint,
          title='API DOCUMENT FOR AUTOMATED RESUME SCREENING',
          version='1.0'
          )

api.add_namespace(user_ns, path='/user')


@api.errorhandler(UnauthorizedError)
def handle_custom_exception(error):
    '''Access denied'''
    return {
        "timestamp": datetime.now().strftime("%Y/%m/%d, %H:%M:%S"),
        "status": 403,
        "error": "Forbidden",
        "message": "Access denied",
        "path": request.url
    }, 403
