from sys import stdout
import pymysql
from app.main import send_email
import datetime

from flask import request, jsonify, url_for, render_template
from flask.wrappers import Response
from flask_restx import Resource

from app.main.resource.parser import register_parser, login_parser
from flask_jwt_extended import (
    jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt, decode_token)
from ..util.dto import AccountDto,CandidateDto
from ..service.account_service import custom_jwt_required, delete_a_account_by_email, get_a_user_by_sername, get_all_users, get_a_user_by_id, get_a_user_by_email, save_changes, set_token, create_token, verify_account
from app.main.service.recruiter_service import insert_new_user_recruiter
from app.main.service.candidate_service import insert_new_user_candidate
from app.main.model.candidate_model import CandidateModel

api = AccountDto.api
_candidate = CandidateDto.api
_account = AccountDto.account
_user_login = AccountDto.account_login


@api.route('/register')
class UserList(Resource):
    #@api.doc('get list user')
    # @api.marshal_list_with(_user, envelope='data')
    # def get(self):
    #     '''List all registered users'''
    #     return get_all_users()

    @api.response(200, 'User register successfully.')
    @api.doc('register a new user')
    @api.expect(_account, validate=True)
    def post(self):
        '''register a new User '''
        data = request.json
        user = get_a_user_by_email(data['email'])

        # if user with email not exist
        if not user:
            try:
                if data["type"] == 0 and data["candidate"]: #type 0 is candidate
                    insert_new_user_candidate(data,data["candidate"])
                elif data["type"] == 1 and data["company"]: #type 1 is candidate
                    insert_new_user_recruiter(data,data["company"])
                else:
                    return {
                        'status': 'failure',
                        'message': 'Registation failed. Unknown type register.',
                    }, 409

                # if account insert successfully
                user_inserted = get_a_user_by_email(data['email'])

                if user_inserted:
                    # send email here
                    try:
                        confirm_url = url_for('api.Account_user_verify',token=user_inserted.access_token, _external=True)
                        html = render_template('email.html', confirm_url = confirm_url)
                        subject = "Please confirm your email"
                        send_email(data['email'], subject, html)
                    except Exception as e: # delete account if send email error
                        delete_a_account_by_email(data['email'])
                        return {
                            'status': 'failure',
                            'message': 'Registation failed. Email not working.'
                        }, 501

                    return {
                        'status': 'success',
                        'message': 'Successfully registered. Please check your email to Verify account.'
                    }, 200
                else:                    
                    return {
                        'status': 'failure',
                        'message': 'Registation failed. Server occur'
                    }, 409
            except Exception as e:
                print(e.args)
                return {
                    'status': 'failure',
                    'message': 'Registation failed. Server occur'
                }, 409
        else:
            # if exist account and verified
            if user.confirmed:
                return {
                    'status': 'failure',
                    'message': 'User already exists. Please Log in.',
                }, 409
            else:
                # resend email if previously expired email
                jwt_data = decode_token(user.access_token)
                if datetime.datetime.now().timestamp() > jwt_data['exp']:
                    access_token = create_token(email=user.email)
                    set_token(user.email, access_token)
                    try:
                        confirm_url = url_for('api.Account_user_verify',token=user.access_token, _external=True)
                        html = render_template('email.html', confirm_url = confirm_url)
                        subject = "Please confirm your email"
                        send_email(data['email'], subject, html)
                    except Exception as e: # delete account if send email error
                        return {
                            'status': 'failure',
                            'message': 'Resend email failure. Email not working.'
                        }, 501
                return {
                    'status': 'failure',
                    'message': 'The account has been created but not verified, please check the email.',
                }, 409


@api.route('/confirm/<token>')
@api.param('token', 'The token Verify')
class UserVerify(Resource):
    @api.doc('Verify user account')
    # @api.marshal_with(_user)
    def get(self, token):
        '''Verify user account'''
        try:
            # decode token to json
            jwt_data = decode_token(token) or None

            # check token valid or expired
            if jwt_data and ('identity' in jwt_data) and datetime.datetime.now().timestamp() < jwt_data['exp']:

                user = get_a_user_by_email(jwt_data['identity'])
                if user and (user.access_token == token):
                    if user.confirmed:
                        return{
                            'status': 'success',
                            'message': 'Account already confirmed. Please login.'
                        }, 200
                    else:
                        verify_account(user.email)
                        return{
                            'status': 'success',
                            'message': 'You have confirmed your account. Thanks!'
                        }, 200
                else:
                    return {
                        'status': 'failure',
                        'message': 'The confirmation link is not found.'
                    }, 404
            else:
                return {
                    'status': 'failure',
                    'message': 'The confirmation link is invalid or has expired.'
                }, 403
        except Exception:
            return{
                'status': 'failure',
                'message': 'Try again'
            }, 420


@ api.route('/<id>')
@ api.param('id', 'The User identifier')
@ api.response(404, 'User not found.')
class UserFind(Resource):
    @ api.doc('get a user')
    @custom_jwt_required
    def get(self, id):
        '''get a user given its identifier'''
        user = get_a_user_by_id(id)
        if not user:
            api.abort(404)
        else:
            return user, 200


@ api.route('/login')
@ api.response(404, 'User not found.')
@ api.expect(_user_login)
class UserLogin(Resource):
    @ api.doc('Login with email, password')
    def post(self):
        '''get a user given its identifier'''
        data = login_parser.parse_args()
        try:
            # find user with email
            try:
                user = get_a_user_by_email(data['email'])
            except Exception:
                user = None

            # if  account not exist
            if not user:
                return {
                    'status': 'failure',
                    'message': 'User doesn\'t exist'
                }, 404

            # check password
            if user.check_password(data['password']):

                try:
                    # account have not been verified
                    if not user.confirmed:

                        # resend email if previously expired email
                        jwt_data = decode_token(user.access_token)
                        if datetime.datetime.now().timestamp() > jwt_data['exp']:
                            access_token = create_token(email=user.email)
                            set_token(user.email, access_token)
                            # send email here
                        return {
                            'status': 'failure',
                            'message': 'The account has been created but not verified, please check the email.',
                        }, 403

                    access_token = create_token(email=user.email)
                    set_token(user.email, access_token)

                    return {
                        'status': 'success',
                        'access_token': access_token,
                        'message': 'Login successfully with email: '+data.email,
                    }, 200
                except Exception:
                    return{
                        'status': 'failure',
                        'message': 'Try again'
                    }, 500
            else:
                return {
                    'status': 'failure',
                    'message': 'Email or password invalid'
                }, 401
        except Exception:
            return{
                'status': 'failure',
                'message': 'Try again'
            }, 500
