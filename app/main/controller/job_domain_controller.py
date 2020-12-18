from app.main.service.job_domain_service import get_all_domain
from ..dto.job_domain_dto import JobDomainDto

from flask_restx import Resource

api = JobDomainDto.api
_domain = JobDomainDto.job_domain

@api.route('')
class JobDomainList(Resource):
    @api.doc('list of job domain')
    def get(self):
        return get_all_domain()