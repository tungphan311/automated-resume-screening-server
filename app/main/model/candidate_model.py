from sqlalchemy.orm import backref
from .. import db, flask_bcrypt


class CandidateModel(db.Model):
    """ candidate Model for storing account related details """
    __tablename__ = "candidate"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), unique=True )
    date_of_birth = db.Column(db.DateTime, nullable=True)
