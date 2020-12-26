from app.main.util.format_text import format_contract
from flask import json
from flask_jwt_extended.utils import get_jwt_identity
from app.main.util.custom_jwt import HR_only
from app.main.dto.job_post_dto import JobPostDto
from flask_restx.inputs import email
from app.main.util.response import json_serial, response_object
import dateutil.parser
from app.main import db
from app.main.model.job_post_model import JobPostModel
from app.main.model.recruiter_model import RecruiterModel
from app.main.model.job_domain_model import JobDomainModel
from app.main.util.data_processing import get_technical_skills
import datetime

api = JobPostDto.api

def add_new_post(post):
    parse_deadline = dateutil.parser.isoparse(post['deadline'])

    recruiter = RecruiterModel.query.filter_by(email=post['recruiter_email']).first()
    job_domain = JobDomainModel.query.get(post['job_domain_id'])

    if (not recruiter) | (not job_domain):
        return "Error"

    (skills, _) = get_technical_skills(job_domain.alternative_name, post['requirement_text'])

    print(skills)

    new_post = JobPostModel(
        job_domain_id=post['job_domain_id'],
        description_text=post['description_text'],
        requirement_text=post['requirement_text'],
        benefit_text=post['benefit_text'],
        job_title=post['job_title'],
        contract_type=post['contract_type'],
        min_salary=post['min_salary'],
        max_salary=post['max_salary'],
        amount=post['amount'],
        technical_skills='|'.join(skills),
        deadline=parse_deadline
    )

    recruiter.job_posts.append(new_post)
    job_domain.job_posts.append(new_post)

    db.session.add(recruiter)
    db.session.add(job_domain)

    db.session.commit()

    return response_object(code=200, message="Đăng tin tuyển dụng thành công.", data=new_post.to_json()), 200

@HR_only
def get_hr_posts(page, page_size, sort_values, is_showing):
    identity = get_jwt_identity()
    email = identity['email']
    hr = RecruiterModel.query.filter_by(email=email).first()

    if is_showing: 
        posts = JobPostModel.query\
            .filter(JobPostModel.recruiter_id == hr.id)\
            .filter((JobPostModel.deadline >= datetime.datetime.now()) & (JobPostModel.closed_in == None))\
            .order_by(*sort_job_list(sort_values))\
            .paginate(page, page_size, error_out=False)
    else:
        posts = JobPostModel.query\
            .filter(JobPostModel.recruiter_id == hr.id)\
            .filter((JobPostModel.deadline < datetime.datetime.now()) | (JobPostModel.closed_in != None))\
            .order_by(*sort_job_list(sort_values))\
            .paginate(page, page_size, error_out=False)

    res = [{ 
        'id': post.id, 
        'job_title': post.job_title, 
        'salary': 'Thoả thuận', 
        'posted_in': json.dumps(post.posted_in, default=json_serial),
        'deadline': json.dumps(post.deadline, default=json_serial),
        'total_view': post.total_views,
        'total_save': post.total_views,
        'total_apply': post.total_applies
    } for post in posts.items ]

    pagination = {
        'total': posts.total,
        'page': posts.page
    }

    return response_object(code=200, message="Lấy danh sách thành công", data=res, pagination=pagination)


def candidate_get_job_posts():
    return "Can"


def sort_job_list(sort_values):
    posted_in = sort_values['posted_in']
    deadline = sort_values['deadline']
    view = sort_values['view']
    apply = sort_values['apply']
    save = sort_values['save']

    res = []

    if posted_in == -1:
        res.append(JobPostModel.posted_in.desc())
    elif posted_in == 1:
        res.append(JobPostModel.posted_in.asc())

    if deadline == -1:
        res.append(JobPostModel.deadline.desc())
    elif deadline == 1:
        res.append(JobPostModel.deadline.asc())

    if view == -1:
        res.append(JobPostModel.total_views.desc())
    elif view == 1:
        res.append(JobPostModel.total_views.asc())

    if apply == -1:
        res.append(JobPostModel.total_applies.desc())
    elif apply == 1:
        res.append(JobPostModel.total_applies.asc())

    if save == -1:
        res.append(JobPostModel.total_saves.desc())
    elif save == 1:
        res.append(JobPostModel.total_saves.asc())

    return res


def count_jobs():
    identity = get_jwt_identity()
    email = identity['email']
    hr = RecruiterModel.query.filter_by(email=email).first()

    is_showing = JobPostModel.query\
            .filter(JobPostModel.recruiter_id == hr.id)\
            .filter((JobPostModel.deadline >= datetime.datetime.now()) & (JobPostModel.closed_in == None))\
            .count()

    is_closed = JobPostModel.query\
            .filter(JobPostModel.recruiter_id == hr.id)\
            .filter((JobPostModel.deadline < datetime.datetime.now()) | (JobPostModel.closed_in != None))\
            .count()

    return response_object(code=200, message="", data={ "is_showing": is_showing, "is_closed": is_closed })


@HR_only
def hr_get_detail(id):
    post = JobPostModel.query.get(id)

    if not post:
        return response_object(code=400, message="Thao tác không hợp lệ")

    response = {
        'id': post.id, 
        'job_title': post.job_title, 
        'job_domain': post.job_domain.name,
        'salary': 'Thoả thuận', 
        'posted_in': json.dumps(post.posted_in, default=json_serial),
        'deadline': json.dumps(post.deadline, default=json_serial),
        'contract_type': format_contract(post.contract_type),
        'amount': post.amount,
        'description': post.description_text,
        'requirement': post.requirement_text,
        'benefit': post.benefit_text,
        'total_view': post.total_views,
        'total_save': post.total_views,
        'total_apply': post.total_applies,
    }

    return response_object(200, "Thành công.", response)
