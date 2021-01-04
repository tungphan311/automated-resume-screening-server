from flask_restx import Namespace, fields
from app.main.dto.base_dto import base

class MajorDto:
    api = Namespace("Major", description='major related operation')

    major = api.model('major', {
        'id': fields.Integer(required=True, description='id of major'),
        'name': fields.String(required=True, description='name of major'),
    })

    major_list = api.inherit("majors", base, {
        'data': fields.Nested(major)
    })