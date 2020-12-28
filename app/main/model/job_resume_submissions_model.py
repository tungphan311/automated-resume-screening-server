from app.main.model.job_post_model import JobPostModel
from app.main.model.resume_model import ResumeModel
from .. import db
from datetime import datetime

class JobResumeSubmissionModel(db.Model):
    __tablename__ = "job_resume_submissions"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    resume_id = db.Column(db.Integer, db.ForeignKey(ResumeModel.id), nullable=False)

    job_post_id = db.Column(db.Integer, db.ForeignKey(JobPostModel.id), nullable=False)

    submit_date = db.Column(db.DateTime, default=datetime.now)
    score = db.Column(db.Float, nullable=True)

    process_status = db.Column(db.Boolean, nullable=True)
    score_array = db.Column(db.String(100), nullable=True)
    score_explanation_array = db.Column(db.String(100), nullable=True)

    is_calculating = db.Column(db.Boolean, default=False)
