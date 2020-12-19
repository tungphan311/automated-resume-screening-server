from flask_jwt_extended.utils import get_jwt_identity
from app.main.util.custom_jwt import HR_only
from flask import app, request

from ..dto.job_post_dto import JobPostDto
from flask_restx import Resource
from ..service.job_post_service import add_new_post, candidate_get_job_posts, get_hr_posts

api = JobPostDto.api
_job_post = JobPostDto.job_post


@api.route('')
class JobPost(Resource):
    @api.doc('add a new job post')
    @api.expect(_job_post, validate=True)
    @HR_only
    def post(self):
        data = request.json
        return add_new_post(data)

    @api.doc('get list of job post')
    def get(self):
        is_hr = request.args.get('is_hr') == 'true'

        page = request.args.get('page', app.config['DEFAULT_PAGE'], type=int)
        page_size = request.args.get('page-size', app.config['DEFAULT_PAGE_SIZE'], type=int)

        if is_hr:
            return get_hr_posts(page, page_size)
        else:
            return candidate_get_job_posts()
