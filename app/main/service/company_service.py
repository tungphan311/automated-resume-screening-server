from app.main import db
from app.main.model.company_model import CompanyModel


def get_all_company():
    return CompanyModel.query.all()

def get_a_company_by_name(name):
    return CompanyModel.query.filter_by(name=name).first()