from flask_restx import Namespace, fields

from app.main.model.company_model import CompanyModel

class CompanyDto:
    api = Namespace(
        'Company', description='company related operations')
    company = api.model('company', {
        'name': fields.String(required=True, description='company name'),
        'location': fields.String(required=True, description='company location'),
        'phone': fields.String(required=True, description='company phone number'),
        'email': fields.String(required=True, description='company email'),
        'logo': fields.String(required=False, description='company logo'),
        'background': fields.String(required=False, description='company background'),
        'website': fields.String(required=True, description='company website'),
        'description': fields.String(required=True, description='company description'),
    })

class CandidateDto:
    api = Namespace(
        'Candidate', description='candidate related operations')
    candidate = api.model('candidate', {
        'email': fields.String(required=True, description='user email address'),
        'password': fields.String(required=True, description='user password'),
        'fullName': fields.String(required=True, description='user full name'),
        'phone': fields.String(required=True, description='user phone'),
        'gender': fields.Boolean(required=True, description='user gender'),
        'dateOfBirth': fields.DateTime(required=True, description='candidate birthday'),
    })
    profile = api.model('candidate', {
        'email': fields.String(required=True, description='user email address'),
        'fullName': fields.String(required=True, description='user full name'),
        'phone': fields.String(required=True, description='user phone'),
        'gender': fields.Boolean(required=True, description='user gender'),
        'dateOfBirth': fields.DateTime(required=True, description='candidate birthday'),
        'provinceId': fields.Integer(required=False , description='province_id'),
    })
    account = api.model('account', {
        'email': fields.String(required=True, description='user email address'),
        'password': fields.String(required=True, description='user password'),
    })

class RecruiterDto:
    api = Namespace(
        'Recruiter', description='Recruiter related operations')
    recruiter = api.model('recruiter', {
        'email': fields.String(required=True, description='user email address'),
        'password': fields.String(required=True, description='user password'),
        'fullName': fields.String(required=True, description='user full name'),
        'phone': fields.String(required=True, description='user phone'),
        'gender': fields.Boolean(required=True, description='user gender'),
    })
    account = api.model('account', {
        'email': fields.String(required=True, description='user email address'),
        'password': fields.String(required=True, description='user password'),
    })

class AccountDto:
    api = Namespace(
        'Account', description='account related operations')

    company = api.model('account_company', {
        'companyName': fields.String(required=True, description='user email address'),
        'companyLocation': fields.String(required=True, description='user email address'),
        'companyPhone': fields.String(required=True, description='user email address'),
        'companyEmail': fields.String(required=True, description='user email address'),
        'companyLogo': fields.String(required=True, description='user email address'),
        'companyWebsite': fields.String(required=True, description='user email address'),
        'companyDescription': fields.String(required=True, description='user email address'),
    })

    candidate = api.model('candidate_company', {
        'dateOfBirth': fields.DateTime(required=True, description='candidate birthday'),
    })

    account = api.model('account', {
        'email': fields.String(required=True, description='user email address'),
        'password': fields.String(required=True, description='user password'),
        'fullName': fields.String(required=True, description='user full name'),
        'phone': fields.String(required=True, description='user phone'),
        'gender': fields.Boolean(required=True, description='user gender'),
        'isCandidate': fields.Boolean(required=True, description='true is candidate, false is recruiter'),
        'company' : fields.Nested(company,allow_null=True),
        'candidate' : fields.Nested(candidate,allow_null=True),
    })
    account_login = api.model('account_login', {
        'email': fields.String(required=True, description='user email address'),
        'password': fields.String(required=True, description='user password'),
    })