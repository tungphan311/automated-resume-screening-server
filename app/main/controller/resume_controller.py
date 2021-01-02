from app.main.service.account_service import create_token
from app.main.service.candidate_service import get_a_account_candidate_by_email
from flask_jwt_extended.utils import get_jwt_identity
from app.main.util.custom_jwt import Candidate_only
from flask_restx.fields import String
from app.main.service.resume_service import create_cv, get_resume_by_candidate_id, get_resume_by_id, update_cv
from flask.globals import request
from flask_restx import Namespace
from flask_restx import Resource
from flask import jsonify
import os
import uuid
from werkzeug.datastructures import FileStorage
from app.main.util.response import response_object
from app.main.dto.resume_dto import ResumeDTO

api = ResumeDTO.api

# New resume parser
create_resume_parser = api.parser()
create_resume_parser.add_argument("file", type=FileStorage, location="files", required=True)

@api.route("/")
class CV(Resource):
    @api.doc('post a new resume')
    @api.expect(create_resume_parser)
    @api.marshal_with(ResumeDTO.create_success, code=200)
    @Candidate_only
    def post(self):
        args = create_resume_parser.parse_args()
        file = args["file"]
        filename = file.filename.split('.', 1)[0]
        file_ext = file.filename.split('.', 1)[1]

        filepath = os.path.join("temp_pdf", "res_{uid}.pdf".format(uid=str(uuid.uuid4().hex)))
        file.save(filepath)
        data = create_cv(filepath, args, filename, file_ext)
        return response_object(data=data)




# Update resume parser
update_cv_parser = api.parser()
update_cv_parser.add_argument("resume_id", location="json", required=True)
update_cv_parser.add_argument("educations", location="json", required=True)
update_cv_parser.add_argument("experiences", location="json", required=True)
update_cv_parser.add_argument("skills", location="json", required=True)
update_cv_parser.add_argument("months_of_experience", type=int, location="json", required=True)

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



@api.route("/candidate-list-cv")
class CV(Resource):
    @api.doc('get list CV candidate by token')
    @Candidate_only
    def get(self):
        identity = get_jwt_identity()
        candidate = get_a_account_candidate_by_email(identity['email'])
        resumes = get_resume_by_candidate_id(candidate.id)
        if not resumes:
            return response_object(data = None ,message ="Data null or empty"),200
        return response_object(data = [resume.to_json() for resume in resumes],message ="successfully")

@api.route("/findById")
class CV(Resource):
    @api.doc('get list CV candidate by token')
    @api.param('id', 'id of resume')
    def get(self):
        resumeId = request.args.get('id')
        if not resumeId:
            return response_object(data=None, message = "Missing query id", code = 400), 400
        resume = get_resume_by_id(resumeId)
        if not resume:
            return response_object(data=None, message = "failure"), 200
        return response_object(data = resume.to_json(),message ="successfully")
