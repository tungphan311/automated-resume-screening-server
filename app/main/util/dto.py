from flask_restx import Namespace, fields

from app.main.model.company_model import CompanyModel
from app.main.dto.base_dto import base
from app.main.dto.resume_dto import ResumeDTO
from app.main.dto.job_post_dto import JobPostDto

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
        'province_id': fields.String(required=True, description='candidate location'),
    })
    profile = api.model('candidate', {
        'email': fields.String(required=True, description='user email address'),
        'fullName': fields.String(required=True, description='user full name'),
        'phone': fields.String(required=True, description='user phone'),
        'gender': fields.Boolean(required=True, description='user gender'),
        'dateOfBirth': fields.DateTime(required=True, description='candidate birthday'),
        'provinceId': fields.Integer(required=True , description='province_id'),
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
        'resumes': fields.Nested(ResumeDTO.resume_detail_fields)
    })
    candidate_detail_response = api.inherit('candidate_detail_response', base, {
        'data': fields.Nested(candidate_detail_fields)
    })

    ####################
    # Get saved job posts
    ####################
    saved_job_post_fields = api.model("saved_job_post_fields", {
        'id': fields.Integer, 
        'recruiter_id': fields.Integer, 
        'resume_id': fields.Integer, 
        'created_on': fields.DateTime(),
        'job_post': fields.Nested(JobPostDto.job_post_for_cand_fields),
    })
    pagination = api.model('pagination', {
        'page': fields.Integer,
        'total': fields.Integer,
    })
    get_saved_job_post_list_response = api.inherit('get_saved_job_post_list_response', base, {
        'data': fields.List(fields.Nested(saved_job_post_fields)),
        'pagination': fields.Nested(pagination)
    })

    ########################
    # Get applied job posts
    ########################
    applied_job_post_fields = api.model("applied_job_post_fields", {
        'id': fields.Integer,
        'resume_id': fields.Integer,
        'job_post_id': fields.Integer,
        'submit_date': fields.DateTime(),
        'job_post': fields.Nested(JobPostDto.job_post_for_cand_fields),
    })
    get_applied_job_post_list_response = api.inherit('get_applied_job_post_list_response', base, {
        'data': fields.List(fields.Nested(applied_job_post_fields)),
        'pagination': fields.Nested(pagination)
    })

    ########################
    # Get uploaded resumes
    ########################
    single_resume = api.model("single_resume", {
        'id': fields.Integer,
        'resume_filename': fields.String,
        'resume_file_extension': fields.String,
        'store_url': fields.String
    })
    resume_list = api.inherit('resume_list', base, {
        'data': fields.List(fields.Nested(single_resume)),
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

    ####################
    # Get saved resumes
    ####################
    resume_detail_fields = api.model("resume_detail_fields", {
        'id': fields.Integer,
        'months_of_experience': fields.Integer,
        'cand_id': fields.Integer,
        'cand_linkedin': fields.String,
        'cand_github': fields.String,
        'cand_facebook': fields.String,
        'cand_twitter': fields.String,
        'cand_mail': fields.String,
        'cand_phone': fields.String,
        'soft_skills': fields.String,
        'technical_skills': fields.String,
        'store_url': fields.String,
        'is_finding_job': fields.Boolean,
        'resume_filename': fields.String,
        'resume_file_extension': fields.String,
        'total_views': fields.Integer,
        'total_saves': fields.Integer,
        'educations': fields.String,
        'experiences': fields.String,
        'job_domain_id': fields.Integer,

        'job_domain_name': fields.String(attribute='job_domain.name'),
        'cand_name': fields.String(attribute='candidate.full_name'),
        'cand_email': fields.String(attribute='candidate.email'),
        'cand_phone_from_user_input': fields.String(attribute='candidate.phone'),
    })
    saved_resume_info_fields = api.model("saved_resume_info_fields", {
        'id': fields.Integer, 
        'recruiter_id': fields.Integer, 
        'resume_id': fields.Integer, 
        'created_on': fields.DateTime(),
        'resume': fields.Nested(resume_detail_fields),
    })
    pagination = api.model('pagination', {
        'page': fields.Integer,
        'total': fields.Integer,
    })
    get_saved_resume_list_response = api.inherit('get_saved_resume_list_response', base, {
        'data': fields.List(fields.Nested(saved_resume_info_fields)),
        'pagination': fields.Nested(pagination)
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