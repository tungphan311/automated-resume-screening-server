from app.main.model.major_model import MajorModel
from app.main.dto.major_dto import MajorDto
from flask_restx import Resource
from app.main.util.response import response_object

api = MajorDto.api

@api.route("")
class Major(Resource):
    @api.doc('get major list')
    @api.marshal_with(MajorDto.major_list, code=200)
    def get(self):
        majors = MajorModel.query.all()

        return response_object(data=majors)