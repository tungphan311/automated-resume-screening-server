from os import name
from app.main import db
from app.main.util.response import response_object
from app.main.model.company_model import CompanyModel


def get_all_company():
    return CompanyModel.query.all()

def get_a_company_by_name(name, page, page_size=5):
    query = CompanyModel.query.filter(CompanyModel.name.contains(name)).paginate(page, page_size, error_out=False)

    companies = [ com for com in query.items ]
    has_next = query.has_next

    return companies, has_next


def add_new_company(data, logo, background):
    company = CompanyModel(
        name=data['name'], 
        location=data['location'],
        phone=data['phone'],
        email=data['email'],
        website=data['website'],
        description=data['description']
    )

    db.session.add(company)
    db.session.commit()
    
    return response_object(200, "Cập nhật thông tin công ty thành công")