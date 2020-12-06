from sqlalchemy.orm import backref
from .. import db, flask_bcrypt


class RecruiterModel(db.Model):
    """ Recruiter Model for storing user related details """
    __tablename__ = "recruiter"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), unique=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), unique=True)