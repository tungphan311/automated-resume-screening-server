from app.main.util.response import response_object
from app.main.model.job_domain_model import JobDomainModel

def get_all_domain():
    domains = JobDomainModel.query.all()
    domains = [ d.to_json() for d in domains ]

    return response_object(code=200, message="Lấy danh sách domain thành công", data=domains)