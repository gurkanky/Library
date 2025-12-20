from flask import request
from functools import wraps

def debug_jwt(f):
    """JWT token debug middleware"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization', None)
        print(f"[JWT Debug] Endpoint: {request.path}")
        print(f"[JWT Debug] Authorization Header: {auth_header}")
        print(f"[JWT Debug] All Headers: {dict(request.headers)}")
        return f(*args, **kwargs)
    return decorated_function

