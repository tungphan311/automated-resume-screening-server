from app.main.util.response import response_object
from os import abort
from app.main.model.filter_candidates import FilterCandidateModel
from app.main.model.recruiter_model import RecruiterModel
from flask_jwt_extended.utils import get_jwt_identity
from app.main import db


def add_new_filter(data):
    identity = get_jwt_identity()
    email = identity['email']
    hr = RecruiterModel.query.filter_by(email=email).first()

    new_filter = FilterCandidateModel(
        name=data['name'],
        job_domains=data['job_domains'] or None,
        provinces=data['provinces'] or None,
        atleast_skills=data['atleast_skills'] or None,
        required_skills=data['required_skills'] or None,
        not_allowed_skills=data['not_allowed_skills'] or None
    )

    try:
        hr.fiter_candidates.append(new_filter)
        db.session.add(hr)
        db.session.commit()
    except:
        abort(400)


    return response_object(message="Tạo bộ lọc mới thành công", data=new_filter.id)


def get_filter_list(args):
    page = args.get('page')
    page_size = args.get('page-size')

    result = FilterCandidateModel.query.paginate(page, page_size, error_out=False)

    return result.items, {
        'total': result.total,
        'page': result.page
    }