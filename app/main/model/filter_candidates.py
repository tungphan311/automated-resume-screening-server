from .. import db
from datetime import datetime

class FilterCandidateModel(db.Model):
    __tablename__ = "filter_candidates"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    job_domains = db.Column(db.String(100), nullable=True)
    provinces = db.Column(db.String(100), nullable=True)
    atleast_skills = db.Column(db.String(300), nullable=True)
    required_skills = db.Column(db.String(300), nullable=True)
    not_allowed_skills = db.Column(db.String(300), nullable=True)
    min_year = db.Column(db.String(10), nullable=True)
    max_year = db.Column(db.String(10), nullable=True)
    gender = db.Column(db.Integer, nullable=True)
    months_of_experience = db.Column(db.Integer, nullable=True)
    last_edit = db.Column(db.DateTime, nullable=False, default=datetime.now)

    recruiter_id = db.Column(db.Integer, db.ForeignKey('recruiters.id'), nullable=False)
