from sqlalchemy.orm import backref
from app.main.util.response import json_serial
from flask import json
from app.main.model.job_domain_model import JobDomainModel
from .. import db

class JobPostModel(db.Model):
    __tablename__ = "job_posts"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    recruiter_id = db.Column(db.Integer, db.ForeignKey('recruiters.id'), nullable=False)
    job_domain_id = db.Column(db.Integer, db.ForeignKey(JobDomainModel.id), nullable=False)

    description_text = db.Column(db.Text, nullable=False)
    requirement_text = db.Column(db.Text, nullable=False)
    benefit_text = db.Column(db.Text, nullable=False)

    technical_skills = db.Column(db.String(500), nullable=True)
    soft_skills = db.Column(db.String(500), nullable=True)

    total_views = db.Column(db.Integer, default=0)
    total_saves = db.Column(db.Integer, default=0)

    job_post_detail = db.relationship("JobPostDetailModel", uselist=False, backref="job_post")
    job_resume_submissions = db.relationship('JobResumeSubmissionModel', backref="job_post", lazy=True)

    def __repr__(self):
        return "<Job post: '{}'>".format(self.id)

    def to_json(self):
        return {
            'title': self.job_post_detail.job_title,
            'recruiter': self.recruiter_id,
            'job_domain': self.job_domain_id,
            'description': self.description_text,
            'requirement': self.requirement_text,
            'benefit': self.benefit_text,
            'contract': self.job_post_detail.contract_type,
            'min_salary': self.job_post_detail.min_salary,
            'max_salary': self.job_post_detail.max_salary,
            'amount': self.job_post_detail.amount,  
            'is_active': self.job_post_detail.is_active,  
            'deadline': json.dumps(self.job_post_detail.deadline, default=json_serial),
            'posted_in': json.dumps(self.job_post_detail.posted_in, default=json_serial),
            'last_edit': json.dumps(self.job_post_detail.last_edit, default=json_serial),
            'closed_in': json.dumps(self.job_post_detail.closed_in, default=json_serial),
        }