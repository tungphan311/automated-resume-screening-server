from app.main.util.dto import CandidateDto
from app.main.service.account_service import create_token
import datetime
from app.main import db
from app.main.model.candidate_model import CandidateModel


def get_a_account_candidate_by_email(email):
    return CandidateModel.query.filter_by(email=email).first()

def get_all_candidate():
    return CandidateModel.query.all()

def insert_new_account_candidate(account):
    new_account = CandidateModel(
        email=account['email'],
        password=account['password'],
        phone = account['phone'],
        full_name = account['fullName'],
        gender = account['gender'],
        date_of_birth = account['dateOfBirth'],
        access_token=create_token(account['email'], 1/24),
        registered_on=datetime.datetime.utcnow()
    )
    db.session.add(new_account)
    db.session.commit()

def delete_a_candidate_by_id(id):
    return CandidateModel.query.filter_by(id=id).first()

def set_token_candidate(email, token):
    account = get_a_account_candidate_by_email(email)
    account.access_token = token
    db.session.add(account)
    db.session.commit()

def verify_account_candidate(email):
    account = get_a_account_candidate_by_email(email)
    account.confirmed = True
    account.confirmed_on = datetime.datetime.utcnow()
    db.session.add(account)
    db.session.commit()

def get_candidate_by_id(id):
    cand = CandidateModel.query.get(id)
    return cand