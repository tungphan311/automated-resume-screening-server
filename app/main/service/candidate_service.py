from app.main.model.job_post_model import JobPostModel
from app.main.util.dto import CandidateDto
from app.main.service.account_service import create_token
import datetime
from app.main import db
from app.main.model.candidate_model import CandidateModel

from app.main.model.candidate_job_save_model import CandidateJobSavesModel
from flask_restx import abort


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


def alter_save_job(cand_email, args):
    job_post_id = args['job_post_id']
    status = args['status']

    #Check candidate
    cand = CandidateModel.query.filter_by(email=cand_email).first()
    if cand is None: abort(400)
    cand_id = cand.id
    
    # Create 
    if status != 0:
        # Check existence.
        jp = JobPostModel.query.get(job_post_id)
        if jp is None: abort(400)

        existed = CandidateJobSavesModel.query\
            .filter_by(cand_id=cand_id, job_post_id=job_post_id)\
            .first()
        if existed is None:
            existed = CandidateJobSavesModel(
                cand_id=cand_id,
                job_post_id=job_post_id,
            )
            db.session.add(existed)
            db.session.commit()

        return {
            'id': existed.id,
            'cand_id': existed.cand_id,
            'job_post_id': existed.job_post_id
        }

    # Remove
    if status == 0:
        # Check existence.
        remove = CandidateJobSavesModel.query\
            .filter_by(cand_id=cand_id, job_post_id=job_post_id)\
            .first()
        if remove is None: abort(400)

        db.session.delete(remove)
        db.session.commit()

        return {
            'id': remove.id,
            'job_post_id': remove.job_post_id,
            'cand_id': remove.cand_id
        }
