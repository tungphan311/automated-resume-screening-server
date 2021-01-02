from app.main.model.recruiter_model import RecruiterModel
from app.main.model.candidate_model import CandidateModel
from app.main.model.job_post_model import JobPostModel
from app.main.model.resume_model import ResumeModel
from .. import db
from datetime import datetime


class RecruiterResumeSavesModel(db.Model):
    __tablename__ = "recruiter_resume_saves"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    recruiter_id = db.Column(db.Integer, db.ForeignKey(RecruiterModel.id), nullable=False)
    resume_id = db.Column(db.Integer, db.ForeignKey(ResumeModel.id), nullable=False)