from datetime import datetime

def response_object(code = 200, message = "Thành công.", data = []):
    return {
        'code': code,
        'message': message,
        'data': data
    }

def json_serial(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()