from flask_restx.fields import String
from app.main.util.response import response_object
from app.main.service.filter_service import add_new_filter, find_candidates, get_filter_list
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


find_candidates_parser = api.parser()

# Today, 3 days, 7 days, ...
find_candidates_parser.add_argument("job_domains", type=int, action="split", location="args", required=False)
# fulltime (0), parttime (1), internship (2)
find_candidates_parser.add_argument("provinces", action="split", location="args", required=False)
find_candidates_parser.add_argument("atleast_skills", action="split", location="args", required=False)
find_candidates_parser.add_argument("not_allowed_skills", action="split", location="args", required=False)
find_candidates_parser.add_argument("required_skills", action="split", location="args", required=False)

find_candidates_parser.add_argument("page", type=int, location="args", required=False, default=1)
find_candidates_parser.add_argument("page-size", type=int, location="args", required=False, default=10)
find_candidates_parser.add_argument("min_year", type=int, location="args", required=False)
find_candidates_parser.add_argument("max_year", type=int, location="args", required=False)
find_candidates_parser.add_argument("gender", location="args", required=False)
find_candidates_parser.add_argument("months_of_experience", type=int, location="args", required=False)
@api.route('/candidates')
class FilterCandidateDetail(Resource):
    @api.doc('find candidate with filter id')
    @api.marshal_with(FilterDto.candidate_list, code=200)
    # @HR_only
    def get(self):
        args = find_candidates_parser.parse_args()
        data, pagination = find_candidates(args)

        return response_object(data=data, pagination=pagination)