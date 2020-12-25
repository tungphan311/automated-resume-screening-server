from app.main.util.resume_extractor import ResumeExtractor
from app.main.util.firebase import Firebase
from app.main.util.thread_pool import ThreadPool
from app.main import db




def create_cv(cv_local_path):
    executor = ThreadPool.instance().executor
    info_res = executor.submit(ResumeExtractor(cv_local_path).segment_cv)
    url_res = executor.submit(Firebase().upload, cv_local_path)

    resume_info = info_res.result()
    remote_path = url_res.result()

    return {
        "test": "ok",
        "a": resume_info,
        "b": remote_path
    }, 200

    