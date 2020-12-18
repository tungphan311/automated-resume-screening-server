from app.main.util.constant import HR
from app.main.util.custom_jwt import HR_only
from flask import request

from ..dto.job_post_dto import JobPostDto
from flask_restx import Resource
from ..service.job_post_service import add_new_post

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