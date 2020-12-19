from flask_jwt_extended.utils import get_jwt_identity
from app.main.util.custom_jwt import HR_only
from app.main.dto.job_post_dto import JobPostDto
from flask_restx.inputs import email
from app.main.util.response import response_object
import dateutil.parser
from app.main import db
from app.main.model.job_post_model import JobPostModel
from app.main.model.job_post_detail_model import JobPostDetailModel
from app.main.model.recruiter_model import RecruiterModel
from app.main.model.job_domain_model import JobDomainModel

api = JobPostDto.api

def add_new_post(post):
    parse_deadline = dateutil.parser.isoparse(post['deadline'])

    recruiter = RecruiterModel.query.filter_by(email=post['recruiter_email']).first()
    job_domain = JobDomainModel.query.get(post['job_domain_id'])

    if (not recruiter) | (not job_domain):
        return "Error"

    job_post_detail = JobPostDetailModel(
        job_title=post['job_title'],
        contract_type=post['contract_type'],
        min_salary=post['min_salary'],
        max_salary=post['max_salary'],
        amount=post['amount'],
        deadline=parse_deadline
    )

    new_post = JobPostModel(
        job_domain_id=post['job_domain_id'],
        description_text=post['description_text'],
        requirement_text=post['requirement_text'],
        benefit_text=post['benefit_text'],
    )
    new_post.job_post_detail = job_post_detail

    recruiter.job_posts.append(new_post)
    job_domain.job_posts.append(new_post)

    db.session.add(recruiter)
    db.session.add(job_domain)
    db.session.add(new_post)
    db.session.commit()

    return response_object(code=200, message="Đăng tin tuyển dụng thành công", data=new_post.to_json()), 200

@HR_only
def get_hr_posts(page, page_size):
    identity = get_jwt_identity()
    email = identity['email']

    hr = RecruiterModel.query.filter_by(email=email).first()

    posts = [ post.to_json() for post in hr.job_posts ]
    return response_object(code=200, message="Lấy danh sách thành công", data=posts)


def candidate_get_job_posts():
    return "Can"