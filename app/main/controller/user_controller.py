import datetime
from flask import request, jsonify
from flask.wrappers import Response
from flask_restx import Resource

from app.main.resource.parser import register_parser, login_parser
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)
from app.main.model.user_model import UserModel
from ..util.dto import UserDto
from ..service.user_service import custom_jwt_required, insert_new_user, get_all_users, get_a_user_by_id, get_a_user_by_email, save_changes, set_token

api = UserDto.api
_user = UserDto.user
_user_login = UserDto.user_login


@api.route('/register')
class UserList(Resource):
    @api.doc('get list user')
    @api.marshal_list_with(_user, envelope='data')
    def get(self):
        '''List all registered users'''
        return get_all_users()

    @api.response(201, 'User register successfully.')
    @api.doc('register a new user')
    @api.expect(_user, validate=True)
    def post(self):
        '''register a new User '''
        data = register_parser.parse_args()
        if not get_a_user_by_email(data.email):
            try:
                user = insert_new_user(data)
                print(user)
                if get_a_user_by_email(data.email):
                    return {
                        'status': 'success',
                        'message': 'Successfully registered.'
                    }, 201
                else:
                    return {
                        'status': 'fail',
                        'message': 'Can not create this user with email: '+data.email,
                    }, 409
            except Exception:
                return {
                    'status': 'fail',
                    'message': 'Can not create this user with email: '+data.email,
                }, 409
        else:
            return {
                'status': 'fail',
                'message': 'User already exists. Please Log in.',
            }, 409


@ api.route('/<id>')
@ api.param('id', 'The User identifier')
@ api.response(404, 'User not found.')
class UserFind(Resource):
    @ api.doc('get a user')
    @ api.marshal_with(_user)
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
            try:
                user = get_a_user_by_email(data['email'])
            except Exception:
                user = None

            if not user:
                return {
                    'message': 'User {} doesn\'t exist'.format(data.username)
                }, 404

            if user.check_password(data['password']):                
                expires = datetime.timedelta(days=7)
                access_token = create_access_token(
                    identity=user.email, expires_delta=expires)
                set_token(user.email, access_token)
                return {
                    'status': 'success',
                    'access_token': access_token,
                    'message': 'Login successfully with email: '+data.email,
                }, 200
            else:
                return {
                    'status': 'failure',
                    'message': 'Email or password invalid'
                }, 401
        except Exception as e:
            return{
                'status': 'failure',
                'message': 'Try again'
            }, 500
