from .. import db

class CandidateEducationModel(db.Model):
    __tablename__ = "candidate_education"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    school_name = db.Column(db.String(255), nullable=False)
    from_date = db.Column(db.DateTime, nullable=False)
    to_date = db.Column(db.DateTime, nullable=True)
    degree_level = db.Column(db.Integer, nullable=False)
    major = db.Column(db.String(255), nullable=False)

    resume_id = db.Column(db.Integer, db.ForeignKey("resumes.id"), nullable=False)
