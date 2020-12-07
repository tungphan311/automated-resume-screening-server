from sys import stdout
import pymysql
import datetime

from flask import request, jsonify, url_for, render_template
from flask.wrappers import Response
from flask_restx import Resource

from app.main import insert_token_to_backlist, send_email
from app.main.resource.parser import register_parser, login_parser
from flask_jwt_extended import (
    jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt, decode_token)
from ..util.dto import AccountDto,CandidateDto
from ..service.account_service import delete_a_account_by_email, get_a_account_by_sername, get_all_accounts, get_all_accounts, get_a_account_by_id, get_a_account_by_email, save_changes, set_token, create_token, verify_account
from app.main.service.recruiter_service import insert_new_account_recruiter
from app.main.service.candidate_service import insert_new_account_candidate

api = AccountDto.api
_account = AccountDto.account
_account_login = AccountDto.account_login


@api.route('/register')
class AccountList(Resource):
    @api.doc('get list account')
    def get(self):
        '''List all registered account'''
        return get_all_accounts()

    @api.response(200, 'account register successfully.')
    @api.doc('register a new account')
    @api.expect(_account, validate=True)
    def post(self):
        '''register a new account '''
        data = request.json
        account = get_a_account_by_email(data['email'])

        # if account with email not exist
        if not account:
            try:
                if data["isCandidate"] == True and data["candidate"]: #type 0 is candidate
                    insert_new_account_candidate(data,data["candidate"])
                elif data["isCandidate"] == False and data["company"]: #type 1 is candidate
                    insert_new_account_recruiter(data,data["company"])
                else:
                    return {
                        'status': 'failure',
                        'message': 'Registation failed. Unknown type register.',
                    }, 409
                # if account insert successfully
                account_inserted = get_a_account_by_email(data['email'])

                if account_inserted:
                    # send email here
                    try:
                        confirm_url = url_for('api.Account_account_verify',token=account_inserted.access_token, _external=True)
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
            if account.confirmed:
                return {
                    'status': 'failure',
                    'message': 'account already exists. Please Log in.',
                }, 409
            else:
                # resend email if previously expired email
                jwt_data = decode_token(account.access_token)
                if datetime.datetime.now().timestamp() > jwt_data['exp']:
                    access_token = create_token(email=account.email)
                    set_token(account.email, access_token)
                    try:
                        confirm_url = url_for('api.Account_account_verify',token=account.access_token, _external=True)
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
class AccountVerify(Resource):
    @api.doc('Verify account account')
    def get(self, token):
        '''Verify account account'''
        try:
            # decode token to json
            jwt_data = decode_token(token) or None

            # check token valid or expired
            if jwt_data and ('identity' in jwt_data) and datetime.datetime.now().timestamp() < jwt_data['exp']:

                account = get_a_account_by_email(jwt_data['identity'])
                if account and (account.access_token == token):
                    if account.confirmed:
                        return{
                            'status': 'success',
                            'message': 'Account already confirmed. Please login.',
                            'auth_token': account.access_token
                        }, 200
                    else:
                        verify_account(account.email)
                        return{
                            'status': 'success',
                            'message': 'You have confirmed your account. Thanks!',
                
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
@ api.param('id', 'The Account identifier')
@ api.response(404, 'Account not found.')
class AccountFind(Resource):
    @ api.doc('get a Account')
    @jwt_required
    def get(self, id):
        '''get a Account given its identifier'''
        account = get_a_account_by_id(id)
        if not account:
            api.abort(404)
        else:
            return account, 200


@ api.route('/login')
@ api.response(404, 'account not found.')
@api.expect(_account_login, validate=True)
class AccountLogin(Resource):
    @ api.doc('Login with email, password')
    def post(self):
        '''get a account given its identifier'''
        data = login_parser.parse_args()
        try:
            # find account with email
            try:
                account = get_a_account_by_email(data['email'])
            except Exception:
                account = None

            # if  account not exist
            if not account:
                return {
                    'status': 'failure',
                    'message': 'Wrong email or password'
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
                            set_token(account.email, access_token)
                            # send email here
                        return {
                            'status': 'failure',
                            'message': 'The account has been created but not verified, please check the email.',
                        }, 403

                    access_token = create_token(email=account.email)
                    set_token(account.email, access_token)

                    return {
                        'status': 'success',
                        'access_token': access_token,
                        'message': 'Login successfully with email: '+data.email,
                    }, 200
                except Exception as e:
                    print(e.args)
                    return{
                        'status': 'failure',
                        'message': 'Try again'
                    }, 500
            else:
                return {
                    'status': 'failure',
                    'message': 'Email or password invalid'
                }, 401
        except Exception as e:
            print(e.args)
            return{
                'status': 'failure',
                'message': 'Try again'
            }, 500

@ api.route('/logout')
@ api.expect(_account_login)
class AccountLogout(Resource):
    @ api.doc('Logout this session')
    @jwt_required
    def delete(self):
        jti = get_raw_jwt()['jti']
        insert_token_to_backlist(jti)
        return jsonify({"msg": "Successfully logged out"}), 200
