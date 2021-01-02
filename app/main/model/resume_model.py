from flask import json
from sqlalchemy import inspection
from .. import db
from app.main.model.job_domain_model import JobDomainModel

class ResumeModel(db.Model):
    __tablename__ = "resumes"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    months_of_experience = db.Column(db.Integer, nullable=True)
    cand_id = db.Column(db.Integer, db.ForeignKey("candidates.id"), nullable=False)
    cand_linkedin = db.Column(db.String(200), nullable=True)
    cand_github = db.Column(db.String(200), nullable=True)
    cand_facebook = db.Column(db.String(200), nullable=True)
    cand_twitter = db.Column(db.String(200), nullable=True)
    cand_mail = db.Column(db.String(200), nullable=True)
    cand_phone = db.Column(db.String(15), nullable=True)
    soft_skills = db.Column(db.Text, nullable=True)
    technical_skills = db.Column(db.Text, nullable=True)
    store_url =  db.Column(db.String(200), nullable=False)
    is_finding_job = db.Column(db.Boolean, default=False)
    job_resume_submission = db.relationship('JobResumeSubmissionModel', uselist=False, backref="resume")

    resume_filename = db.Column(db.String(100), nullable=False)
    resume_file_extension = db.Column(db.String(10), nullable=False)

    total_views = db.Column(db.Integer, default=0)
    total_saves = db.Column(db.Integer, default=0)
    
    educations = db.Column(db.Text, nullable=True)
    experiences = db.Column(db.Text, nullable=True)

    job_domain_id = db.Column(db.Integer, db.ForeignKey(JobDomainModel.id), nullable=True)

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}   

    def to_json(self):
        return {
            "id": self.id,
            "months_of_experience": self.months_of_experience,
            "candidate_profile": self.candidate.to_json(),
            "cand_linkedin": self.cand_linkedin,
            "cand_github": self.cand_github,
            "cand_facebook": self.cand_facebook,
            "cand_twitter": self.cand_twitter,
            "cand_mail": self.cand_mail,
            "cand_phone": self.cand_phone,
            "soft_skills": self.soft_skills,
            "technical_skills": self.technical_skills,
            "store_url": self.store_url,
            "is_finding_job": self.is_finding_job,
            "resume_filename": self.resume_filename,
            "resume_file_extension": self.resume_file_extension,
            "total_views": self.total_views,
            "total_saves": self.total_saves,
            "educations": self.educations,
            "experiences": self.experiences,
            "job_domain": self.job_domain.to_json()
        }