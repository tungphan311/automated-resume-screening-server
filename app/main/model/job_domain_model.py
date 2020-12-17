from sqlalchemy.orm import backref
from .. import db

class JobPostModel(db.Model):
    __tablename__ = "job_domains"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)

    job_posts = db.relationship("JobPostModel", backref="job_domain", lazy=True)

    def __repr__(self):
        return "<Job domains: '{}'>".format(self.name)