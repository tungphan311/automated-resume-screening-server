from app.main.controller import job_post_controller
from sys import float_info
from app.main.service.matching_service import OnetoOneMatching, jobPipeline
import datetime
from datetime import datetime, timedelta
import dateutil.parser
from flask import json
from app.main import db
from app.main.dto.job_post_dto import JobPostDto
from app.main.model.resume_model import ResumeModel
from app.main.model.job_post_model import JobPostModel
from app.main.model.recruiter_model import RecruiterModel
from app.main.model.job_resume_submissions_model import JobResumeSubmissionModel
from app.main.model.job_domain_model import JobDomainModel

from flask_jwt_extended.utils import get_jwt_identity
from app.main.util.custom_jwt import HR_only
from app.main.util.format_text import format_contract
from app.main.util.response import json_serial, response_object
from app.main.util.data_processing import get_technical_skills
from flask_restx import abort
from sqlalchemy import or_
from app.main.business.matching import Matcher
from app.main.util.thread_pool import ThreadPool

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


def update_jp(id, recruiter_email, args):
    job_post = JobPostModel.query.get(id)
    recruiter = RecruiterModel.query.filter_by(email=recruiter_email).first()
    if job_post == None or\
        recruiter == None or\
        job_post.recruiter_id != recruiter.id:
        abort(400)
    
    job_domain_id = args.get("job_domain_id", None)
    description_text = args.get("description_text", None)
    requirement_text = args.get("requirement_text", None)
    benefit_text = args.get("benefit_text", None)
    job_title = args.get("job_title", None)
    contract_type = args.get("contract_type", None)
    min_salary = args.get("min_salary", None)
    max_salary = args.get("max_salary", None)
    amount = args.get("amount", None)
    is_active = args.get("is_active", None)
    deadline = args.get("deadline", None)

    if job_domain_id is None: job_post.job_domain_id = job_domain_id
    if description_text is None: job_post.description_text = description_text
    if requirement_text is None: job_post.requirement_text = requirement_text
    if benefit_text is None: job_post.benefit_text = benefit_text
    if job_title is None: job_post.job_title = job_title
    if min_salary is None: job_post.min_salary = max(min_salary, 0)
    if max_salary is None: job_post.max_salary = min(max_salary, float_info.max)
    if amount is None: job_post.amount = amount
    if is_active is None: job_post.is_active = is_active
    if deadline is None: job_post.deadline = deadline
    if contract_type is None and contract_type <= 2 and contract_type >= 0: 
        job_post.contract_type = contract_type

    job_post.last_edit = datetime.now
    db.session.commit()
    return job_post



def close_jp(id, recruiter_email):
    job_post = JobPostModel.query.get(id)
    recruiter = RecruiterModel.query.filter_by(email=recruiter_email).first()
    if job_post == None or\
        recruiter == None or\
        job_post.recruiter_id != recruiter.id:
        abort(400)

    job_post.is_active = False
    job_post.closed_in = datetime.now
    db.session.commit()
    return job_post()

    

def apply_cv_to_jp(jp_id, args):
    resume_id = args['resume_id']

    if ResumeModel.query.get(resume_id) == None:
        abort(400)

    if JobPostModel.query.get(jp_id) == None:
        abort(400)

    submission = JobResumeSubmissionModel(
        resume_id=resume_id,
        job_post_id=jp_id,
        is_calculating=True,
    )

    db.session.add(submission)
    db.session.commit()

    # Start calculating score
    __background_calculate_scrore(submission.id, jp_id, resume_id)
    # res = ThreadPool.instance().executor.submit(__background_calculate_scrore, submission.id, jp_id, resume_id)
    # _ = res.result()
    
    return {
        "id": submission.id,
        "resume_id": submission.resume_id,
        "job_post_id": submission.job_post_id,
        "is_calculating": submission.is_calculating
    }

def __background_calculate_scrore(submission_id, job_post_id, resume_id):
    submission = JobResumeSubmissionModel.query.get(submission_id)
    if submission == None: return

    score_dict = OnetoOneMatching(resume_id=resume_id, job_id=job_post_id)
    skill_score = score_dict['skill_match']
    domain_skill_scrore = score_dict['domain_skill_match']
    
    score_explanation_array = '|'.join(['skill_match', 'domain_skill_match'])
    score_array = '|'.join([skill_score, domain_skill_scrore])
    submission.is_calculating = False
    submission.score_array = score_array
    submission.score_explanation_array = score_explanation_array
    db.session.commmit()
    return True
    

    
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


def delete_job_post(ids):
    for id in ids:
        job = JobPostModel.query.get(id)

        if not job:
            abort(400)

        db.session.delete(job)

    db.session.commit()

    return response_object(message="Xoá tin tuyển dụng thành công")


def proceed_resume(id, recruiter_email, args):
    submission_id = args['submission_id']
    status = args['status']
    job_post = JobPostModel.query.get(id)
    recruiter = RecruiterModel.query.filter_by(email=recruiter_email).first()
    submission = JobResumeSubmissionModel.query.get(submission_id)

    if job_post == None or\
        recruiter == None or\
        submission == None or\
        job_post.recruiter_id != recruiter.id or\
        submission.job_post_id != id:
        abort(400)

    if status != 0 or status != 1:
        abort(400)

    submission.process_status = status
    db.session.commit()
    return submission
