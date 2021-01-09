from flask_restx import fields

class NullableFloat(fields.Float):
    __schema_type__ = ['number', 'null']
    __schema_example__ = 'nullable float'

class NullableString(fields.String):
    __schema_type__ = ['string', 'null']
    __schema_example__ = 'nullable string'

class NullableInteger(fields.Integer):
    __schema_type__ = ['integer', 'null']
    __schema_example__ = 'nullable integer'

class NullableBoolean(fields.Boolean):
    __schema_type__ = ['boolean', 'null']
    __schema_example__ = 'nullable boolean'