from app.main.service.resume_service import cv_segmentation, remove_temp_files
from flask.globals import request
from flask_restx import Namespace
from flask_restx import Resource
import os

api = Namespace('Upload files', description="upload file related operation")

@api.route("/cv")
class CV(Resource):
    @api.doc('post a new CV')
    def post(self):
        remove_temp_files('temp_pdf/*')
        file = request.files['file']
        file.save(os.path.join("temp_pdf", "CV.pdf"))

        return cv_segmentation()
        
