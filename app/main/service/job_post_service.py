import sqlalchemy
from app.main.util.format_text import format_contract
from datetime import datetime, timedelta
from app.main.model.resume_model import ResumeModel
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
from app.main.model.job_resume_submissions_model import JobResumeSubmissionModel
from app.main.model.candidate_model import CandidateModel
from app.main.model.job_domain_model import JobDomainModel
from app.main.util.data_processing import get_technical_skills
import datetime
from flask_restx import abort
from sqlalchemy import func
from sqlalchemy import or_

api = JobPostDto.api

def add_new_post(post):
    parse_deadline = dateutil.parser.isoparse(post['deadline'])

    recruiter = RecruiterModel.query.filter_by(email=post['recruiter_email']).first()
    job_domain = JobDomainModel.query.get(post['job_domain_id'])

    if (not recruiter) | (not job_domain):
        return "Error"

    (skills, _) = get_technical_skills(job_domain.alternative_name, post['requirement_text'])

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
        'total_save': post.total_saves,
        'total_apply': post.total_applies,
    }

    return response_object(200, "Thành công.", response)
    

def apply_cv_to_jp(jp_id, args):
    resume_id = args['resume_id']

    if ResumeModel.query.get(resume_id) == None:
        abort(400)

    if JobPostModel.query.get(jp_id) == None:
        abort(400)

    submission = JobResumeSubmissionModel(
        resume_id=resume_id,
        job_post_id=jp_id,
        submit_date=datetime.now,
        score=0
    )

    db.session.add(submission)
    db.session.commit()

    return submission

    
def get_job_post_for_candidate(jp_id):
    post = JobPostModel.query.get(jp_id)
    if not post:
        abort(400)

    post.total_views += 1

    db.session.add(post)
    db.session.commit()

    return post


def search_jd_for_cand(args):
    query = JobPostModel.query
    posted_date = args.get('posted_date')
    contract_type = args.get('contract_type')
    min_salary = args.get('min_salary')
    max_salary = args.get('max_salary')
    page = args.get('page')
    page_size = args.get('page-size')
    keyword = args.get('q')
    province_id = args.get('province_id')

    if contract_type is not None:   
        query = query.filter(JobPostModel.contract_type == contract_type)

    if min_salary is not None:
        query = query.filter(or_(\
            JobPostModel.max_salary == None,\
            JobPostModel.max_salary >= min_salary)\
        )

    if max_salary is not None:
        query = query.filter(or_(\
            JobPostModel.min_salary == None,\
            JobPostModel.min_salary >= max_salary)\
        )

    if keyword is not None:
        key = "%{word}%".format(word=keyword)
        query = query.filter(JobPostModel.job_title.ilike(key))

    # if not province_id:
    #     query = query.filter(JobPostModel.province_id == province_id)

    if posted_date is not None: 
        query = query.filter((datetime.datetime.now() - timedelta(days=posted_date)) < JobPostModel.posted_in)

    result = query\
        .order_by(JobPostModel.last_edit)\
        .paginate(page=page, per_page=page_size)
    
    return result.items, {
        'total': result.total,
        'page': result.page
    }