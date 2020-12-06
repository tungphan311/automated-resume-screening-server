from app.main.service.company_service import get_a_company_by_name
from flask_restx import Resource
from flask import jsonify
from flask_jwt_extended import jwt_required
from ..util.dto import CompanyDto

api = CompanyDto.api

@api.route('/<name>')
@api.response(404, 'Company not found.')
class CompanyFind(Resource):
    @ api.doc('Find list companies')
    @jwt_required
    def get(self,name):
        '''get list companies by name'''
        company = get_a_company_by_name(name)
        print(company)
        if not company:
            print("vào")
            return{

            },400
        else:
            return jsonify(company)