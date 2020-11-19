from flask import Flask
from flask_bcrypt import Bcrypt
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy

from .config import config_by_name

db = SQLAlchemy()
flask_bcrypt = Bcrypt()
mail = Mail()
app = Flask(__name__)


def create_app(config_name):
    app = Flask(__name__, static_folder='../../static', static_url_path='/')
    app.config.from_object(config_by_name[config_name])
    db.init_app(app)
    flask_bcrypt.init_app(app)
    return app


def send_email(to, subject, template):
    msg = Message(
        subject,
        recipients=[to],
        html=template,
        sender='automated.resume.screening@gmail.com'
    )
    mail.send(msg)
