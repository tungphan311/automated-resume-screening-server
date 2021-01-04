from .. import db
from sqlalchemy.orm import backref

class MajorModel(db.Model):
    __tablename__ = "majors"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)

    candidates = db.relationship("CandidateEducationModel", backref=backref("major", lazy="joined"), lazy=True)