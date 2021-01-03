from logging import StreamHandler
from flask_restx import Namespace, Model, fields
from app.main.dto.base_dto import base

class ResumeDTO:
    api = Namespace('Resumes', description="Resume related operation.")

    __base = api.model("base", base)


    # CREATE RESUME
    cv_data_success = api.inherit('create_data_success', {
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
        'total_views': fields.Integer,
        'total_saves': fields.Integer,
        'experiences': fields.String,
        'educations': fields.String,
    })
    create_success = api.inherit('create_success', base, {
        "data": fields.Nested(cv_data_success)
    })
    update_success = api.inherit('update_success', base, {
        "data": fields.Nested(cv_data_success)
    })

    ######################
    # Resume detail model
    ######################
    resume_detail_fields = api.model('resume_detail_fields', {
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
        # Relations
        # 'job_resume_submission'
    })