from functools import wraps
from flask import session, redirect, url_for

def checkLogin(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if "user" not in session:  ## jika belum login
            return redirect(url_for("login_index")) ## redirect ke halaman login
        else: ##jika sudah,
            return func(*args, **kwargs) ## lanjut ke halaman yang dituju
            
    return decorated_function