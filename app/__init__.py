from os import error
from flask_restx import Api
from flask import Blueprint

from .main.controller.user_controller import api as user_ns
from app.main.resource.errors import errors

blueprint = Blueprint('api', __name__)

api = Api(blueprint,
          title='FLASK RESTX API BOILER-PLATE WITH JWT',
          error=errors,
          version='1.0',
          description='a boilerplate for flask restplus web service'
          )

api.add_namespace(user_ns, path='/api/user')