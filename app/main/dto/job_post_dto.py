from app.main.util.custom_fields import NullableFloat
from flask_restx import Namespace, fields, Model
from app.main.dto.base_dto import base
from app.main.util.format_text import format_contract, format_salary

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

    job_list = api.model('job_list', {
        'id': fields.Integer(description='id of job post'),
        'job_title': fields.String(description='job title'),
        'salary': fields.String(description='salary for candidate'),
        'posted_in': fields.DateTime(description='when did this post?'),
        'deadline': fields.DateTime(description='last day for candidate to apply'),
        'total_apply': fields.Integer(description='nums of candidate who applied this post'),
        'new_apply': fields.Integer(description='nums of candidate who applied this post recently'),
        'total_view': fields.Integer(description='nums of candidate who viewed this post'),
    })



    # Response job post for cand
    job_post_for_cand_fields = api.model("job_post_for_cand_fields", {
        'id': fields.Integer, 
        'job_title': fields.String, 
        'job_domain': fields.String(attribute='job_domain.name'),
        'salary': fields.String(attribute=lambda x: format_salary(x.min_salary, x.max_salary)), 
        'posted_in': fields.DateTime(),
        'deadline': fields.DateTime,
        'contract_type': fields.String(attribute=lambda x: format_contract(x.contract_type)),
        'description': fields.String(attribute='description_text'),
        'requirement': fields.String(attribute='requirement_text'),
        'benefit': fields.String(attribute='benefit_text'),
        'amount': fields.Integer,
        'company_name': fields.String(attribute=lambda x: x.recruiter.company.name),
        'company_logo': fields.String(attribute=lambda x: x.recruiter.company.logo),
        'company_background': fields.String(attribute=lambda x: x.recruiter.company.background),
        # 'total_view': fields. post.total_views,
        # 'total_save': fields. post.total_views,
        # 'total_apply': fields. post.total_applies,
    })
    job_post_for_cand = api.inherit('job_post_for_cand', base, {
        'data': fields.Nested(job_post_for_cand_fields)
    })



    # Response for search job post
    single_job_post_in_search_fields = api.model("single_job_post_in_search_fields", {
        'job_title': fields.String,
        'company_name': fields.String(attribute=lambda x: x.recruiter.company.name),
        'last_edit': fields.DateTime(),
        'salary': fields.String(attribute=lambda x: format_salary(x.min_salary, x.max_salary)), # todod
        'contact_type': fields.String(attribute=lambda x: format_contract(x.contract_type)),
        'province_id': fields.String,
        'job_post_id': fields.Integer(attribute=lambda x: x.id),
        'job_description': fields.String(attribute=lambda x: x.description_text),
    })
    pagination = api.model('pagination', {
        'page': fields.Integer,
        'total': fields.Integer,
    })
    job_post_in_search_cand_response = api.inherit('job_post_in_search_cand_response', base, {
        'data': fields.List(fields.Nested(single_job_post_in_search_fields)),
        'pagination': fields.Nested(pagination)
    })