from app.main.util.custom_fields import NullableFloat
from flask_restx import Namespace, fields

class JobPostDto:
    api = Namespace('Job Posts', description='job post related operation')

    job_post = api.model('job_post', {
        'recruiter_email': fields.String(required=True, description='email of hr who post this job'),
        'job_domain_id': fields.Integer(required=True, description='id domain of this post'),
        'description_text': fields.String(required=True, description='job description'),
        'requirement_text': fields.String(required=True, description='job requirement'),
        'benefit_text': fields.String(required=True, description='benefit for candidate'),
        'job_title': fields.String(required=True, description='job title'),
        'contract_type': fields.Integer(required=True, description='type of contract'),
        'min_salary': NullableFloat(required=False, description='minimum salary'),
        'max_salary': NullableFloat(required=False, description='maximum salary'),
        'amount': fields.Integer(required=True, description='amount of candidates is recruiting'),
        'deadline': fields.DateTime(required=True, description='last day for candidate to apply'),
    })