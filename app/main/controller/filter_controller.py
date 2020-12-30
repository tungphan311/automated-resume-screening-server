from app.main.util.response import response_object
from app.main.service.filter_service import add_new_filter, get_filter_list
from app.main.util.custom_jwt import HR_only
from app.main.dto.filter_dto import FilterDto
from flask_restx import Resource
from flask import request

api = FilterDto.api
_filter = FilterDto.filter

get_list_filter_parser = api.parser()
get_list_filter_parser.add_argument("page", type=int, location="args", required=False, default=1)
get_list_filter_parser.add_argument("page-size", type=int, location="args", required=False, default=10)

@api.route('')
class FilterCandidate(Resource):
    @api.doc('add new filter candidate')
    @api.expect(_filter, validate=True)
    @HR_only
    def post(self):
        data = request.json
        return add_new_filter(data)

    @api.doc('get list of filter')
    @api.expect(get_list_filter_parser)
    @api.marshal_with(FilterDto.filter_response_list, code=200)
    @HR_only
    def get(self):
        args = get_list_filter_parser.parse_args()
        data, pagination = get_filter_list(args)

        return response_object(data=data, pagination=pagination)