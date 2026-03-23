from functools import wraps
from flask import abort
from flask_login import current_user


def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwds):
        if not current_user.is_authenticated:
            abort(401)
        if not current_user.is_admin:
            abort(403)
        return f(*args, **kwds)
    return wrapper