from flask_restx.fields import String
from flask_restx import Namespace
from flask_restx import Resource
from app.main import classify_manager
from datetime import datetime
import json

api = Namespace('Test', description='Testing')


extract_skills_parser = api.parser()
extract_skills_parser.add_argument("text", location="json", required=True)
extract_skills_parser.add_argument("domain", location="json", required=True)

@api.route('/extract_skills')
class Test(Resource):
    
    @api.doc('Text extraction')    
    @api.expect(extract_skills_parser)
    def post(self):
        args = extract_skills_parser.parse_args()

        start=datetime.now()

        result = classify_manager.run_classifier(\
            domain=args["domain"], \
            job_description=args["text"], \
            explanation=True)

        time = datetime.now() - start

        return {
            "result": json.dumps(result.get_dict()),
            "time": time.seconds
        }, 200