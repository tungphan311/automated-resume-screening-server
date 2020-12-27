from app.main.model.candidate_model import CandidateModel
from flask_jwt_extended.utils import get_jwt_identity
from app.main.util.resume_extractor import ResumeExtractor, remove_temp_files
from app.main.util.firebase import Firebase
from app.main.util.thread_pool import ThreadPool
from app.main import db
from app.main.model.resume_model import ResumeModel
import os


def create_cv(cv_local_path, args):
    identity = get_jwt_identity()
    email = identity['email']

    candidate = CandidateModel.query.filter_by(email=email).first()
    
    executor = ThreadPool.instance().executor
    info_res = executor.submit(ResumeExtractor(cv_local_path).extract)
    url_res = executor.submit(Firebase().upload, cv_local_path)

    resume_info = info_res.result()
    remote_path = url_res.result()

    if os.path.exists(cv_local_path): 
        os.remove(cv_local_path)

    resume = ResumeModel(
        months_of_experience=0,
        cand_id=candidate.id,
        cand_linkedin=resume_info['linkedin'],
        cand_github=resume_info['github'],
        cand_facebook=resume_info['facebook'],
        cand_twitter=resume_info['twitter'],
        cand_mail=resume_info['email'],
        cand_phone=resume_info['phone'],
        soft_skills="",
        technical_skills="|".join(resume_info['tech_skills']),
        store_url=remote_path,
        is_finding_job=False,
        total_views=0,
        total_saves=0,
        educations=resume_info["educations"],
        experiences=resume_info["experiences"],
    )

    db.session.add(resume)
    db.session.commit()

    return resume


def update_cv(args):
    resume = ResumeModel.query.get(args['resume_id'])
    resume.resume_id = args['resume_id']
    resume.educations = args['educations']
    resume.experiences = args['experiences']
    resume.skills = args['skills']
    resume.months_of_experience = args['months_of_experience']
    db.session.commit()
    return resume

    