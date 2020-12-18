from .. import db
from datetime import datetime

class JobPostDetailModel(db.Model):
    __tablename__ = "job_post_detail"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    job_post_id = db.Column(db.Integer, db.ForeignKey('job_posts.id'), nullable=False, unique=True)
    
    job_title = db.Column(db.String(200), nullable=False)
    contract_type = db.Column(db.Integer, nullable=False)

    min_salary = db.Column(db.Float, nullable=True)
    max_salary = db.Column(db.Float, nullable=True)

    amount = db.Column(db.Integer, nullable=False)
    is_active = db.Column(db.Boolean, nullable=False, default=True)

    deadline = db.Column(db.DateTime, nullable=False)
    posted_in = db.Column(db.DateTime, nullable=False, default=datetime.now)
    last_edit = db.Column(db.DateTime, nullable=False, default=datetime.now)
    closed_in = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return "<Job post detail: '{}'>".format(self.job_title)