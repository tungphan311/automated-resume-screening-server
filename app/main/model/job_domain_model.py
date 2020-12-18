from sqlalchemy.orm import backref
from .. import db

class JobDomainModel(db.Model):
    __tablename__ = "job_domains"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    alternative_name = db.Column(db.String(255), nullable=False)

    job_posts = db.relationship("JobPostModel", backref=backref("job_domain", lazy="joined"), lazy=True)

    def __repr__(self):
        return "<Job domains: '{}'>".format(self.name)