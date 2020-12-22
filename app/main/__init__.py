from flask import Flask
from flask_jwt_extended import JWTManager
from flask_jwt_extended.utils import get_raw_jwt
from flask_bcrypt import Bcrypt
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy


from .config import config_by_name
from app.process_data.classify_wrapper.classify_manager import ClassifyManager


db = SQLAlchemy()
flask_bcrypt = Bcrypt()
mail = Mail()
app = Flask(__name__)
jwt = JWTManager(app)
blacklist = set()
classifyManager = ClassifyManager()

def create_app(config_name):
    app = Flask(__name__, static_folder='../../static', static_url_path='/')
    app.config.from_object(config_by_name[config_name])
    app.config['JWT_BLACKLIST_ENABLED'] = True
    app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
    db.init_app(app)
    flask_bcrypt.init_app(app)
    jwt = JWTManager(app)
    @jwt.token_in_blacklist_loader
    def check_token_in_blacklist(token_dict: dict) -> bool:
        jti = token_dict['jti']
        return jti in blacklist
    return app


def send_email(to, subject, template):
    msg = Message(
        subject,
        recipients=[to],
        html=template,
        sender='automated.resume.screening@gmail.com'
    )
    mail.send(msg)

# @jwt.token_in_blacklist_loader
# def check_if_token_in_blacklist(decrypted_token):
#     jti = decrypted_token['jti']
#     return jti in blacklist

def insert_token_to_backlist(token):
    blacklist.add(token)
