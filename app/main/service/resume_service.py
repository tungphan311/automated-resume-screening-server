from app.main.util.resume_extractor import ResumeExtractor
from app.main.util.firebase import Firebase
from app.main.util.thread_pool import ThreadPool
from app.main import db
from app.main.model.resume_model import ResumeModel



def create_cv(cv_local_path, args):
    executor = ThreadPool.instance().executor
    info_res = executor.submit(ResumeExtractor(cv_local_path).extract)
    url_res = executor.submit(Firebase().upload, cv_local_path)

    resume_info = info_res.result()
    remote_path = url_res.result()

    resume = ResumeModel(
        months_of_experience=0,
        cand_id=args['cand_id'],
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
    )

    db.session.add(resume)
    db.session.commit()

    return resume

    