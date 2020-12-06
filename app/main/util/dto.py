from flask_restx import Namespace, fields

from app.main.model.company_model import CompanyModel

class CompanyDto:
    api = Namespace(
        'Company', description='company related operations')
    company = api.model('company', {
        'name': fields.String(required=True, description='user email address'),
        'location': fields.String(required=True, description='user email address'),
        'phone': fields.String(required=True, description='user email address'),
        'email': fields.String(required=True, description='user email address'),
        'logo': fields.String(required=True, description='user email address'),
        'website': fields.String(required=True, description='user email address'),
        'description': fields.String(required=True, description='user email address'),
    })

class CandidateDto:
    api = Namespace(
        'Candidate', description='candidate related operations')
    candidate = api.model('candidate', {
        'date_of_birth': fields.DateTime(required=True, description='candidate birthday'),
    })

class AccountDto:
    api = Namespace(
        'Account', description='account related operations')

    company = api.model('company', {
        'name': fields.String(required=True, description='user email address'),
        'location': fields.String(required=True, description='user email address'),
        'phone': fields.String(required=True, description='user email address'),
        'email': fields.String(required=True, description='user email address'),
        'logo': fields.String(required=True, description='user email address'),
        'website': fields.String(required=True, description='user email address'),
        'description': fields.String(required=True, description='user email address'),
    })

    candidate = api.model('candidate', {
        'date_of_birth': fields.DateTime(required=True, description='candidate birthday'),
    })

    account = api.model('account', {
        'email': fields.String(required=True, description='user email address'),
        'password': fields.String(required=True, description='user password'),
        'full_name': fields.String(required=True, description='user full name'),
        'phone': fields.String(required=True, description='user phone'),
        'gender': fields.Boolean(required=True, description='user gender'),
        'type': fields.Integer(required=True, description='0 is candidate, 1 is recruiter'),
        'company' : fields.Nested(company,allow_null=True),
        'candidate' : fields.Nested(candidate,allow_null=True),
    })
    account_login = api.model('account_login', {
        'email': fields.String(required=True, description='user email address'),
        'password': fields.String(required=True, description='user password'),
    })