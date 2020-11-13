from flask import Blueprint
from flask_restx import Api

from .main.controller.user_controller import api as user_ns

blueprint = Blueprint('api', __name__, url_prefix="/api")

api = Api(blueprint,
          title='API DOCUMENT FOR AUTOMATED RESUME SCREENING',
          version='1.0'
          )

api.add_namespace(user_ns, path='/user')
