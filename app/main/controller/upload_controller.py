# from app.main.service.resume_service import create_cv
# from flask.globals import request
# from flask_restx import Namespace
# from flask_restx import Resource
# import os
# import uuid

# api = Namespace('Upload files', description="upload file related operation")


# # New resume parser
# new_resume_parser = api.parser()


# @api.route("/resume")
# class CV(Resource):
#     @api.doc('post a new resume')
#     def post(self):
#         file = request.files['file']
#         filepath = os.path.join("temp_pdf", "res_{uid}".format(uid=str(uuid.uuid4().hex)))
#         file.save(filepath)
#         return create_cv(filepath)
        
             