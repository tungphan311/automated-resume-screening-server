from app.main.util.dto import CandidateDto
from app.main.service.account_service import create_token
import datetime
from app.main.model.account_model import AccountModel
from app.main import db
from app.main.model.candidate_model import CandidateModel


def get_all_candidate():
    return CandidateModel.query.all()

def insert_new_account_candidate(account, candidate):
    new_account = AccountModel(
        email=account['email'],
        password=account['password'],
        phone = account['phone'],
        full_name = account['full_name'],
        gender = account['gender'],
        access_token=create_token(account['email'], 1),
        registered_on=datetime.datetime.utcnow()
    )
    new_candidate = CandidateModel(
        date_of_birth = candidate['date_of_birth'],
        account = new_account
    )
    db.session.add(new_account)
    db.session.add(new_candidate)
    db.session.commit()

def delete_a_candidate_by_id(id):
    return CandidateModel.query.filter_by(id=id).first()
