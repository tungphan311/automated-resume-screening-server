from os import error
from datetime import datetime

from flask.globals import request
from flask_restx import Api
from flask import Blueprint

from .main.controller.user_controller import api as user_ns
from app.main.resource.errors import UnauthorizedError

blueprint = Blueprint('api', __name__)

api = Api(blueprint,
          title='FLASK RESTX API BOILER-PLATE WITH JWT',
          version='1.0',
          description='a boilerplate for flask restplus web service'
          )

api.add_namespace(user_ns, path='/api/user')



# config error message
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
