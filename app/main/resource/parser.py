from flask_restx import Resource
from flask_restx import reqparse

register_parser = reqparse.RequestParser()
register_parser.add_argument('email', help = 'Email cannot be blank', required = True )
register_parser.add_argument('username', help = 'Username cannot be blank', required = True)
register_parser.add_argument('password', help = 'Password cannot be blank', required = True)

login_parser = reqparse.RequestParser()
login_parser.add_argument('email', help = 'Email cannot be blank', required = True)
#login_parser.add_argument('username', help = 'Username cannot be blank', required = True)
login_parser.add_argument('password', help = 'Password cannot be blank', required = True)