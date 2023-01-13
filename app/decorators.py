from functools import wraps
from flask import abort, g


def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwds):
        if not (g.user.is_authenticated and g.user.is_admin):
            abort(401)
        return f(*args, **kwds)
    return wrapper
