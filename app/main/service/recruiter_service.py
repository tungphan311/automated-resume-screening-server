import datetime
from app.main.service.account_service import create_token
from app.main.model.company_model import CompanyModel
from app.main.model.account_model import AccountModel
from app.main import db
from app.main.model.recruiter_model import RecruiterModel
from app.main.service.company_service import get_a_company_by_name


def get_all_recruiter():
    return RecruiterModel.query.all()


def insert_new_account_recruiter(account, company):
    instance_company = get_a_company_by_name(company['companyName'])

    if not instance_company:
        print("chưa có company")
        new_account = AccountModel(
            email=account['email'],
            password=account['password'],
            phone = account['phone'],
            full_name = account['fullName'],
            gender = account['gender'],
            access_token=create_token(account['email'], 1/24),
            registered_on=datetime.datetime.utcnow()
        )
        new_company = CompanyModel(
            name = company['companyName'],
            location = company['companyLocation'],
            phone = company['companyPhone'],
            email = company['companyEmail'],
            logo = company['companyLogo'],
            website = company['companyWebsite'],
            description = company['companyDescription'],
        )
        new_recruiter = RecruiterModel(
            account=new_account,
            company=new_company
        )
        db.session.add(new_account)
        db.session.add(new_company)
        db.session.add(new_recruiter)
        db.session.commit()
    else:
        new_account = AccountModel(
            email=account['email'],
            password=account['password'],
            phone = account['phone'],
            full_name = account['fullName'],
            gender = account['gender'],
            access_token=create_token(account['email'], 1/24),
            registered_on=datetime.datetime.utcnow()
        )
        new_recruiter = RecruiterModel(
            account=new_account,
            company=instance_company
        )
        db.session.add(new_account)
        db.session.add(new_recruiter)
        db.session.commit()


def get_a_recruiter_by_email(name):
    return RecruiterModel.query.filter_by(name=name).first()
