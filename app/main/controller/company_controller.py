from flask.globals import request
from app.main.service.company_service import get_a_company_by_name
from flask_restx import Resource
from flask_jwt_extended import jwt_required
from ..util.dto import CompanyDto

api = CompanyDto.api

@api.route('/search')
@api.response(404, 'Company not found.')
class CompanyFind(Resource):
    @ api.doc('Find list companies')
    def get(self):
        '''get list companies by name'''
        name = request.args.get('name')

        try:            
            companies = get_a_company_by_name(name)
        except Exception:
            companies = None

        if not companies:
            return{
                'list':None,
                'size': 0
            },400
        else:
            return{
                'list':[company.to_json() for company in companies],
                'size': len(companies)
            },400
