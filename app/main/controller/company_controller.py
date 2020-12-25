from flask_jwt_extended.utils import get_jwt_identity
from app.main.util.response import response_object
from app.main.util.custom_jwt import HR_only
from flask.globals import request
from app.main.service.company_service import add_new_company, get_a_company_by_name, update_company
from flask_restx import Resource
from ..util.dto import CompanyDto

api = CompanyDto.api
_company = CompanyDto.company

@api.route('/search')
@api.response(404, 'Company not found.')
class CompanyFind(Resource):
    @ api.doc('Find list companies')
    def get(self):
        '''get list companies by name'''
        name = request.args.get('name')
        page = request.args.get('page', 1, type=int)

        companies, has_next = get_a_company_by_name(name, page)
           
        print(companies)

        if not companies:
            return response_object()
        else:
            return response_object(200, "Thành công.", data=[company.to_json() for company in companies], pagination={"has_next": has_next})


@api.route('')
class Company(Resource):
    @api.doc('add a new company')
    @HR_only
    def post(self):
        files = request.files
        data = request.form

        logo = files.get("logo", None)
        background = files.get("background", None)

        identity = get_jwt_identity()
        email = identity['email']

        return add_new_company(data, logo, background, email)


@api.route('/<int:id>/update')
class CompanyUpdate(Resource):
    @api.doc("update HR company")
    @HR_only
    def put(self, id):
        identity = get_jwt_identity()
        email = identity['email']
        
        return update_company(id, email)