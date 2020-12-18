from flask_restx import fields

class NullableFloat(fields.Float):
    __schema_type__ = ['number', 'null']
    __schema_example__ = 'nullable float'