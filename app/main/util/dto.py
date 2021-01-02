from flask_restx import Namespace, fields

from app.main.model.company_model import CompanyModel
from app.main.dto.base_dto import base
from app.main.dto.resume_dto import ResumeDTO

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
    account = api.model('account', {
        'email': fields.String(required=True, description='user email address'),
        'password': fields.String(required=True, description='user password'),
    })

    ########################
    # Candidate detail model
    ########################
    candidate_detail_fields = api.model('candidate_detail_fields', {
        'id': fields.Integer,
        'email': fields.String,
        'password_hash': fields.String,
        'phone': fields.String,
        'full_name': fields.String,
        'gender': fields.Boolean,
        'date_of_birth': fields.DateTime(),
        'status': fields.Integer,
        'province_id': fields.Integer,
        'access_token': fields.String,
        'registered_on': fields.DateTime(),
        'confirmed': fields.Boolean,
        'confirmed_on': fields.DateTime(),
        'resumes': fields.List(fields.Nested(ResumeDTO.resume_detail_fields))
    })
    candidate_detail_response = api.inherit('candidate_detail_response', base, {
        'data': fields.Nested(candidate_detail_fields)
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