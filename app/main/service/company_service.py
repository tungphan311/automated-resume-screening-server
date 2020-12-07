from app.main import db
from sqlalchemy import func
from app.main.model.company_model import CompanyModel


def get_all_company():
    return CompanyModel.query.all()

def get_a_company_by_name(name):
    return CompanyModel.query.filter(CompanyModel.name.contains(name)).all()