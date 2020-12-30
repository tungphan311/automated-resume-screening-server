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
        "id": fields.String,
        "name": fields.String,
        "provinces": fields.String,
        "last_edit": fields.DateTime()
    })
    pagination = api.model('pagination', {
        'page': fields.Integer,
        'total': fields.Integer,
    })

    filter_response_list = api.inherit("filter_response_list", base, {
        'data': fields.List(fields.Nested(single_filter_response)),
        'pagination': fields.Nested(pagination)
    })