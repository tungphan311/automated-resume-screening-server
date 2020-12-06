from app.main.service.account_service import custom_jwt_required
import pymysql
from app.main import send_email
import datetime

from flask import request, jsonify, url_for, render_template
from flask.wrappers import Response
from flask_restx import Resource

from app.main.resource.parser import register_parser, login_parser
from flask_jwt_extended import (
    jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt, decode_token)
from app.main.model.account_model import AccountModel
from ..util.dto import AccountDto, CandidateDto, CompanyDto
from ..service.candidate_service import get_all_candidate

api = CandidateDto.api

@api.route('/')
@api.response(404, 'Company not found.')
class UserFind(Resource):
    @ api.doc('get a company')
    def get(self):
        '''get a user given its identifier'''
        company = get_all_candidate()
        if not company:
            api.abort(404)
        else:
            return company, 200