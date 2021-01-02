from app.main.util.format_text import format_domains, format_experience, format_provinces, format_skill
from app.main.util.custom_fields import NullableString
from flask_restx import Namespace, fields
from app.main.dto.base_dto import base

class FilterDto:
    api = Namespace("Filter Candidates", description='filter candidates related operation')

    filter = api.model("create_filter", {
        'name': fields.String(required=True, description="name of filter candidate"),
        'job_domains': NullableString(required=False, description="list of job domain"),
        'provinces': NullableString(required=False, description="list of province id"), 
        'atleast_skills': NullableString(required=False, description="list of needed skill"),
        'required_skills': NullableString(required=False, description="list of require skill"),
        'not_allowed_skills': NullableString(required=False, description="list of not allowed skill")
    })

    single_filter_response = api.model("single_filter_response", {
        "id": fields.Integer,
        "name": fields.String,
        "provinces": fields.String,
        "last_edit": fields.DateTime()
    })
    pagination = api.model('pagination', {
        'page': fields.Integer,
        'total': fields.Integer,
    })

    filter_detail = api.model("filter_detail", {
        "id": fields.Integer,
        "name": fields.String,
        "provinces": fields.List(fields.String, attribute=lambda x: format_provinces(x.provinces)),
        "domains": fields.List(fields.Integer, attribute=lambda x: format_domains(x.job_domains)),
        "atleast_skills": fields.List(fields.String, attribute=lambda x: x.atleast_skills.split(",") if x.atleast_skills else []),
        "required_skills": fields.List(fields.String, attribute=lambda x: x.required_skills.split(",") if x.required_skills else []),
        "not_allowed_skills": fields.List(fields.String, attribute=lambda x: x.not_allowed_skills.split(",") if x.not_allowed_skills else []),
        "min_year": fields.Integer,
        "max_year": fields.Integer,
        "gender": fields.Boolean,
        "months_of_experience": fields.String,
    })

    filter_detail_response = api.inherit("filter_detail_response", base, {
        'data': fields.Nested(filter_detail)
    })

    filter_response_list = api.inherit("filter_response_list", base, {
        'data': fields.List(fields.Nested(single_filter_response)),
        'pagination': fields.Nested(pagination)
    })

    single_candidate_response = api.model("single_candidate_response", {
        "id": fields.Integer(attribute=lambda x: x.candidate.id),
        "name": fields.String(attribute=lambda x: x.candidate.full_name),
        "total_views": fields.Integer,
        "job_domain": fields.String(attribute=lambda x: x.job_domain.name),
        "province_id": fields.Integer(attribute=lambda x: x.candidate.province_id),
        "experience": fields.String(attribute=lambda x: format_experience(x.months_of_experience)),
        "skills": fields.String(attribute=lambda x: format_skill(x))
    })

    candidate_list = api.inherit("candidate_list", base, {
        'data': fields.List(fields.Nested(single_candidate_response)),
        'pagination': fields.Nested(pagination)
    })