from sqlalchemy.orm import backref
from .. import db

class JobPostModel(db.Model):
    __tablename__ = "job_posts"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    recruiter_id = db.Column(db.Integer, db.ForeignKey('recruiters.id'), nullable=False)
    job_domain_id = db.Column(db.Integer, db.ForeignKey('job_domains.id'), nullable=False)

    description_text = db.Column(db.Text)
    requirement_text = db.Column(db.Text)
    benefit_text = db.Column(db.Text)

    technical_skills = db.Column(db.String(500))
    soft_skills = db.Column(db.String(500))

    job_post_detail = db.relationship("JobPostDetailModel", uselist=False, backref="job_post")

    def __repr__(self):
        return "<Job post: '{}'>".format(self.id)