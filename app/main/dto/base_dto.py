from flask_restx import Resource, fields, Model

base = Model('base', {
    'code': fields.Integer,
    'message': fields.String
})