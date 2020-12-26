from app.main.service.resume_service import create_cv
from flask.globals import request
from flask_restx import Namespace
from flask_restx import Resource
import os
import uuid
from werkzeug.datastructures import FileStorage
from app.main.util.response import response_object
from app.main.dto.resume_dto import ResumeDTO

api = ResumeDTO.api

# New resume parser
create_resume_parser = ResumeDTO.api.parser()
create_resume_parser.add_argument("file", type=FileStorage, location="files", required=True)
create_resume_parser.add_argument("cand_id", type=int, location="form", required=True)

@api.route("/")
class CV(Resource):
    @api.doc('post a new resume')
    @api.expect(create_resume_parser)
    @api.marshal_with(ResumeDTO.create_success, code=200)
    def post(self):
        args = create_resume_parser.parse_args()
        file = args["file"]
        filepath = os.path.join("temp_pdf", "res_{uid}.pdf".format(uid=str(uuid.uuid4().hex)))
        file.save(filepath)
        data = create_cv(filepath, args)
        return response_object(data=data)



        
             