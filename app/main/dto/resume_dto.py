from logging import StreamHandler
from flask_restx import Namespace, Model, fields
from app.main.dto.base_dto import base

class ResumeDTO:
    api = Namespace('Resumes', description="Resume related operation.")



    # CREATE RESUME
    create_data_success = api.inherit('create_data_success', {
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
    })
    create_success = api.inherit('create_success', base, {
        "data": fields.Nested(create_data_success)
    })