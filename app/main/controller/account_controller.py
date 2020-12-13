from app.main.service.account_service import create_token
from sys import stdout

from flask import request, jsonify, url_for, render_template
from flask.wrappers import Response
from flask_restx import Resource

from app.main import insert_token_to_backlist, send_email
from app.main.resource.parser import register_parser, login_parser
from flask_jwt_extended import (
    jwt_required,  get_raw_jwt)
from ..util.dto import AccountDto

api = AccountDto.api
_account = AccountDto.account
_account_login = AccountDto.account_login



# @ api.route('/login')
# @ api.response(404, 'account not found.')
# @api.expect(_account_login, validate=True)
# class AccountLogin(Resource):
#     @ api.doc('Login with email, password')
#     def post(self):
#         '''get a account given its identifier'''
#         data = login_parser.parse_args()
#         try:
#             # find account with email
#             try:
#                 account = get_a_account_by_email(data['email'])
#             except Exception:
#                 account = None

#             # if  account not exist
#             if not account:
#                 return {
#                     'status': 'failure',
#                     'message': 'Wrong email or password'
#                 }, 404

#             # check password
#             if account.check_password(data['password']):

#                 try:
#                     # account have not been verified
#                     if not account.confirmed:

#                         # resend email if previously expired email
#                         jwt_data = decode_token(account.access_token)
#                         if datetime.datetime.now().timestamp() > jwt_data['exp']:
#                             access_token = create_token(email=account.email)
#                             set_token(account.email, access_token)
#                             # send email here
#                         return {
#                             'status': 'failure',
#                             'message': 'The account has been created but not verified, please check the email.',
#                         }, 403

#                     access_token = create_token(email=account.email)
#                     set_token(account.email, access_token)

#                     return {
#                         'status': 'success',
#                         'access_token': access_token,
#                         'message': 'Login successfully with email: '+data.email,
#                     }, 200
#                 except Exception as e:
#                     print(e.args)
#                     return{
#                         'status': 'failure',
#                         'message': 'Try again'
#                     }, 500
#             else:
#                 return {
#                     'status': 'failure',
#                     'message': 'Email or password invalid'
#                 }, 401
#         except Exception as e:
#             print(e.args)
#             return{
#                 'status': 'failure',
#                 'message': 'Try again'
#             }, 500

@ api.route('/logout')
@ api.expect(_account_login)
class AccountLogout(Resource):
    @ api.doc('Logout this session')
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        insert_token_to_backlist(jti)
        return jsonify({"msg": "Successfully logged out"}), 200
