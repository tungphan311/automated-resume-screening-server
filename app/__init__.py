from os import error
from datetime import datetime

from flask.globals import request
from flask_restx import Api
from flask import Blueprint
from flask_restx import Api

from .main.controller.user_controller import api as user_ns
from app.main.resource.errors import UnauthorizedError

blueprint = Blueprint('api', __name__, url_prefix="/api")

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
