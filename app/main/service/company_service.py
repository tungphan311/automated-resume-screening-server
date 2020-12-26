from app.main.util.thread_pool import ThreadPool
from app.main.service.account_service import create_token
from os import name
from app.main import db
from app.main.util.response import response_object
from app.main.model.company_model import CompanyModel
from app.main.model.recruiter_model import RecruiterModel
from app.main import storage


def get_all_company():
    return CompanyModel.query.all()

def get_a_company_by_name(name, page, page_size=5):
    query = CompanyModel.query.filter(CompanyModel.name.contains(name)).paginate(page, page_size, error_out=False)

    companies = [ com for com in query.items ]
    has_next = query.has_next

    return companies, has_next

def upload_image(name, file):
    filename = name + "_" + file.filename.split('.', 1)[0]
    storage.child("images/company/{}.jpg".format(filename)).put(file)
    url = storage.child("images/company/{}.jpg".format(filename)).get_url(None)
    return url

def add_new_company(data, logo, background, email):
    executor = ThreadPool.instance().executor

    logo_res = executor.submit(upload_image, data['name'], logo)
    background_res = executor.submit(upload_image, data['name'], background)

    logo_url = logo_res.result()
    background_url = background_res.result()

    company = CompanyModel(
        name=data['name'], 
        location=data['location'],
        phone=data['phone'],
        email=data['email'],
        website=data['website'],
        description=data['description'],
        logo=logo_url,
        background=background_url
    )

    recruiter = RecruiterModel.query.filter_by(email=email).first()
    company.recruiters.append(recruiter)

    db.session.add(company)
    db.session.commit()

    token = create_token(email=email, is_HR=True, company_id=recruiter.company_id)
    
    return response_object(200, "Cập nhật thông tin công ty thành công", data=token)

def update_company(id, email):
    company = CompanyModel.query.get(id)

    if not company:
        return response_object(400, "Bad request")

    recruiter = RecruiterModel.query.filter_by(email=email).first()

    company.recruiters.append(recruiter)

    db.session.commit()

    token = create_token(email=email, is_HR=True, company_id=recruiter.company_id)

    return response_object(200, "Cập nhật thông tin công ty thành công", data=token)
