from flask_restx import Namespace, fields

class JobDomainDto:
    api = Namespace('Job Domains', description='job domain related operation')

    job_domain = api.model('job_domain', {
        'id': fields.Integer(required=True, description='id of job domain'),
        'name': fields.String(required=True, description='name of job domain'),
        'alternative_name': fields.String(required=True, description='alternative name of job domain')
    })