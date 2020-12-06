from sqlalchemy.orm import backref
from .. import db, flask_bcrypt


class AccountModel(db.Model):
    """ account Model for storing account related details """
    __tablename__ = "account"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    phone = db.Column(db.String(15), nullable=True) 
    full_name = db.Column(db.String(80), nullable=True)
    gender = db.Column(db.Boolean, nullable=False, default=False)

    candidate = db.relationship('CandidateModel', cascade="all,delete",backref=backref("account",uselist=False),uselist=False)
    recruiter = db.relationship('RecruiterModel', cascade="all,delete",backref=backref("account",uselist=False),uselist=False)
    
    access_token = db.Column(db.String(512), nullable=True)
    registered_on = db.Column(db.DateTime, nullable=False)
    confirmed = db.Column(db.Boolean, nullable=False, default=False)
    confirmed_on = db.Column(db.DateTime, nullable=True)

    @property
    def password(self):
        raise AttributeError('password: write-only field')

    @password.setter
    def password(self, password):
        self.password_hash = flask_bcrypt.generate_password_hash(
            password).decode('utf-8')

    def check_password(self, password):
        return flask_bcrypt.check_password_hash(self.password_hash, password)

    def __repr__(self):
        return "<Account '{}'>".format(self.email)
