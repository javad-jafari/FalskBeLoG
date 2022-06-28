from functools import wraps
from flask import  redirect, url_for

from flask_login import current_user

def is_login(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated:
            return redirect(url_for('home'))
        return f(*args, **kwargs)
    return decorated_function 

def is_logout(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.is_anonymous:
            return redirect(url_for('home'))
        return f(*args, **kwargs)
    return decorated_function 