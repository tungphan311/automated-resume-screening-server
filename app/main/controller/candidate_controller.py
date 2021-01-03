from app.main.util.response import response_object
from app.main.util.custom_jwt import Candidate_only, HR_only
from app.main.service.recruiter_service import get_a_account_recruiter_by_email
from app.main import send_email
from app.main.service.account_service import create_token, get_url_verify_email
from flask_jwt_extended import decode_token
import pymysql
import datetime

from app.main.service.candidate_service import get_candidate_by_id, get_candidate_resumes, set_token_candidate,delete_a_candidate_by_id, \
    get_a_account_candidate_by_email, insert_new_account_candidate, verify_account_candidate, \
    get_candidate_by_id, alter_save_job, get_saved_job_posts, get_applied_job_posts

from flask import request, jsonify, url_for, render_template
from flask_restx import Resource, inputs
from app.main.util.dto import CandidateDto
from app.main.util.custom_jwt import get_jwt_identity

apiCandidate = CandidateDto.api
_candidate = CandidateDto.candidate
_candidateAccount = CandidateDto.account
@apiCandidate.route('/candidate/register')
class RegisterCandidateList(Resource):

    @apiCandidate.response(200, 'account register successfully.')
    @apiCandidate.doc('register a new account candidate')
    @apiCandidate.expect(_candidate, validate=True)
    def post(self):
        '''register a new account candiadate '''
        data = request.json
        account = get_a_account_candidate_by_email(data['email'])

        # if account with email not exist
        if not account:
            try:
               
                insert_new_account_candidate(data)

                # if account insert successfully
                account_inserted = get_a_account_candidate_by_email(data['email'])

                if account_inserted:
                    # send email here
                    try:
                        confirm_url = get_url_verify_email(account_inserted.access_token,"candidate")
                        html = render_template('email.html', confirm_url = confirm_url)
                        subject = "Please confirm your email"
                        send_email(data['email'], subject, html)
                        return {
                            'status': 'success',
                            'message': 'Successfully registered. Please check your email to Verify account.',
                            'type':'candidate'
                        }, 200

                    except Exception as e: # delete account if send email error
                        delete_a_candidate_by_id(account_inserted['id'])
                        return {
                            'status': 'failure',
                            'message': 'Registation failed. Email not working.',
                            'type':'candidate'
                        }, 501
                else:                    
                    return {
                        'status': 'failure',
                        'message': 'Registation failed. Server occur',
                        'type':'candidate'
                    }, 409
            except Exception as e:
                return {
                    'status': 'failure',
                    'message': 'Registation failed. Server occur',
                    'type':'candidate'
                }, 409
        else:
            # if exist account and verified
            if account.confirmed:
                return {
                    'status': 'failure',
                    'message': 'Account already exists. Please Log in.',
                    'type': 'candidate',
                }, 409
            else:
                # resend email if previously expired email
                jwt_data = decode_token(account.access_token)
                if datetime.datetime.now().timestamp() > jwt_data['exp']:
                    access_token = create_token(email=account.email)
                    set_token_candidate(account.email, access_token)
                    try:
                        confirm_url = url_for('api.Candidate_candidate_verify',token=account.access_token, _external=True)
                        html = render_template('email.html', confirm_url = confirm_url)
                        subject = "Please confirm your email"
                        send_email(data['email'], subject, html)

                        return{
                            'status': 'success',
                            'message': 'Resend email successful.',
                            'type':'candidate'
                        },200

                    except Exception as e: # delete account if send email error
                        return {
                            'status': 'failure',
                            'message': 'Resend email failure. Email not working.',
                            'type':'candidate'
                        }, 500
                return {
                    'status': 'failure',
                    'message': 'The account has been created but not verified, please check the email.',
                    'type': 'candidate'
                }, 201

@apiCandidate.route('/candidate/confirm/<token>')
@apiCandidate.param('token', 'The token Verify')
class CandidateVerify(Resource):
    @apiCandidate.doc('Verify account account candidate')
    def get(self, token):
        '''Verify account account'''
        try:
            # decode token to json
            jwt_data = decode_token(token) or None

            # check token valid or expired
            if jwt_data and ('identity' in jwt_data) and datetime.datetime.now().timestamp() < jwt_data['exp']:

                account = get_a_account_candidate_by_email(jwt_data['identity']['email'])
                if account and (account.access_token == token):
                    if account.confirmed:
                        return{
                            'status': 'success',
                            'message': 'Account already confirmed. Please login.',
                            'type':"candidate"
                        }, 200
                    else:
                        verify_account_candidate(account.email)
                        return{
                            'status': 'success',
                            'message': 'You have confirmed your account. Thanks!',
                            'type':"candidate"
                        }, 200
                else:
                    return {
                        'status': 'failure',
                        'message': 'The confirmation link is not found.',
                        'type':"candidate"
                    }, 404
            else:
                return {
                    'status': 'failure',
                    'message': 'The confirmation link is invalid or has expired.',
                    'type':"candidate"
                }, 403
        except Exception:
            return{
                'status': 'failure',
                'message': 'Try again'
                ,'type':"candidate"
            }, 420

@apiCandidate.route('/candidate/login')
@apiCandidate.response(404, 'account not found.')
@apiCandidate.expect(_candidateAccount, validate=True)
class AccountLogin(Resource):
    @apiCandidate.doc('Login candidate with email, password')
    @apiCandidate.expect(_candidateAccount, validate=True)
    def post(self):
        '''get a account given its identifier'''
        data = request.json
        try:
            # find account with email
            account = get_a_account_candidate_by_email(data['email'])

            # if  account not exist
            if not account:
                return {
                    'status': 'failure',
                    'message': 'Account not exist',
                    'type':'candidate'
                }, 404

            # check password
            if account.check_password(data['password']):

                try:
                    # account have not been verified
                    if not account.confirmed:

                        # resend email if previously expired email
                        jwt_data = decode_token(account.access_token)
                        if datetime.datetime.now().timestamp() > jwt_data['exp']:
                            access_token = create_token(email=account.email)
                            set_token_candidate(account.email, access_token)
                            # send email here
                        return {
                            'status': 'failure',
                            'message': 'The account has been created but not verified, please check the email.',
                            'type':'candidate'
                        }, 403

                    access_token = create_token(email=account.email)
                    return {
                        'status': 'success',
                        'access_token': access_token,
                        'message': 'Login successfully with email: '+data['email'],
                        'type':'candidate'
                    }, 200
                except Exception as e:
                    return{
                        'status': 'failure',
                        'message': 'Try again',
                        'type':'candidate'
                    }, 500
            else:
                return {
                    'status': 'failure',
                    'message': 'Email or password invalid',
                    'type':'candidate'
                }, 401
        except Exception as e:
            return{
                'status': 'failure',
                'message': 'Try again',
                'type':'candidate'
            }, 500



#################################
#
# Query candidates by id
#
#################################
candidates_by_id_parser = apiCandidate.parser()
candidates_by_id_parser.add_argument("Authorization", location="headers", required=True)
@apiCandidate.route("/candidates/<int:id>")
class QueryCandidates(Resource):
    @apiCandidate.doc("Get candidate by id")
    @apiCandidate.marshal_with(CandidateDto.candidate_detail_response, code=200)
    @apiCandidate.expect(candidates_by_id_parser)
    @HR_only
    def get(self, id): 
        data = get_candidate_by_id(id)
        return response_object(data=data)



###################
# Save Job Post
###################
save_res_parser = apiCandidate.parser()
save_res_parser.add_argument('Authorization', location='headers', required=True)
save_res_parser.add_argument('job_post_id', type=int, location='json', required=True)
save_res_parser.add_argument('status', type=int, location='json', required=True)

get_res_parser = apiCandidate.parser()
get_res_parser.add_argument("Authorization", location="headers", required=False)
get_res_parser.add_argument("page", type=int, location="args", required=False, default=1)
get_res_parser.add_argument("page-size", type=int, location="args", required=False, default=10)
get_res_parser.add_argument("from-date", type=inputs.datetime_from_iso8601, location="args", required=False)
get_res_parser.add_argument("to-date", type=inputs.datetime_from_iso8601, location="args", required=False)

@apiCandidate.route('/job-posts/save')
class SaveResume(Resource):
    @apiCandidate.doc("Save job post")
    @apiCandidate.expect(save_res_parser)
    @Candidate_only
    def post(self):
        identity = get_jwt_identity()
        email = identity['email']
        args = save_res_parser.parse_args()
        data = alter_save_job(email, args)
        return response_object(data=data)

    @apiCandidate.doc("Get saved job posts")
    @apiCandidate.expect(get_res_parser)
    @apiCandidate.marshal_with(CandidateDto.get_saved_job_post_list_response, code=200)
    @Candidate_only
    def get(self):
        identity = get_jwt_identity()
        email = identity['email']
        args = get_res_parser.parse_args()
        (data, pagination) = get_saved_job_posts(email, args)
        return response_object(data=data, pagination=pagination)


@apiCandidate.route('/job-posts/apply')
class GetAppliedJobs(Resource):
    @apiCandidate.doc("Get applied job posts")
    @apiCandidate.expect(get_res_parser)
    @apiCandidate.marshal_with(CandidateDto.get_applied_job_post_list_response, code=200)
    @Candidate_only
    def get(self):
        identity = get_jwt_identity()
        email = identity['email']
        args = get_res_parser.parse_args()
        (data, pagination) = get_applied_job_posts(email, args)
        return response_object(data=data, pagination=pagination)


@apiCandidate.route('/candidates/resumes')
class CandidateResumes(Resource):
    @apiCandidate.doc("Get uploaded resumes")
    @apiCandidate.marshal_with(CandidateDto.resume_list, code=200)
    @Candidate_only
    def get(self):
        identity = get_jwt_identity()
        email = identity['email']

        data = get_candidate_resumes(email)
        return response_object(data=data)
