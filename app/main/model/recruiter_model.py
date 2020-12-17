from sqlalchemy.orm import backref
from .. import db, flask_bcrypt


class RecruiterModel(db.Model):
    """ Recruiter Model for storing account related details """
    __tablename__ = "recruiters"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    phone = db.Column(db.String(15), nullable=True) 
    full_name = db.Column(db.String(80), nullable=True)
    gender = db.Column(db.Boolean, nullable=False, default=False)
    status = db.Column(db.Integer, nullable=True,default=1)

    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), unique=True,nullable=True)
    
    access_token = db.Column(db.String(512), nullable=True)
    registered_on = db.Column(db.DateTime, nullable=False)
    confirmed = db.Column(db.Boolean, nullable=False, default=False)
    confirmed_on = db.Column(db.DateTime, nullable=True)

    job_posts = db.relationship('JobPostModel', backref="recruiter", lazy=True)

    
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
        return "<Recruiter '{}'>".format(self.email)