from flask_restx import Namespace, fields


class ResumeDTO:
    api = Namespace('Resume', description='The object representing resume.')

    new_resume = api.model('job_domain', {
        'id': fields.Integer(required=True, description='id of job domain'),
        'name': fields.String(required=True, description='name of job domain'),
        'alternative_name': fields.String(required=True, description='alternative name of job domain')
    })