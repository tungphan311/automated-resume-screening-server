from sqlalchemy.ext.hybrid import hybrid_method
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

    def __repr__(self):
        return "<Resume '{}'>".format(self.id)

    @hybrid_method
    def contain_at_least_one(self, skills):
        return any(skill in self.technical_skills for skill in skills)