from app.main.util.custom_jwt import Candidate_only
from flask_restx.fields import String
from app.main.service.resume_service import create_cv, update_cv
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
create_resume_parser = api.parser()
create_resume_parser.add_argument("file", type=FileStorage, location="files", required=True)
create_resume_parser.add_argument("Authorization", location="headers", required=True)

@api.route("/")
class CV(Resource):
    @api.doc('post a new resume')
    @api.expect(create_resume_parser)
    @api.marshal_with(ResumeDTO.create_success, code=200)
    @Candidate_only
    def post(self):
        args = create_resume_parser.parse_args()
        file = args["file"]
        file_ext = file.filename.split('.')[-1]
        filename = file.filename.replace(".{}".format(file_ext), "")

        filepath = os.path.join("temp_pdf", "{name}_{uid}.{ext}".format(name=filename, uid=str(uuid.uuid4().hex), ext=file_ext))
        file.save(filepath)
        data = create_cv(filepath, args, filename, file_ext)
        return response_object(data=data)




# Update resume parser
update_cv_parser = api.parser()
update_cv_parser.add_argument("resume_id", type=int, location="json", required=True)
update_cv_parser.add_argument("educations", location="json", required=True)
update_cv_parser.add_argument("experiences", location="json", required=True)
update_cv_parser.add_argument("skills", location="json", required=True)
update_cv_parser.add_argument("months_of_experience", type=int, location="json", required=True)
update_cv_parser.add_argument("job_domain_id", type=int, location="json", required=True)
update_cv_parser.add_argument("Authorization", location="headers", required=True)
@api.route("/update")
class UpdateCV(Resource):
    @api.doc('Update Resume')
    @api.expect(update_cv_parser)
    @api.marshal_with(ResumeDTO.update_success)
    @Candidate_only
    def post(self):
        args = update_cv_parser.parse_args()
        data = update_cv(args)
        return response_object(data=data)
