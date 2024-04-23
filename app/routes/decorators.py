from functools import wraps
from flask import session, redirect, url_for, abort
from ..models.model import User  

# Log in required [Restrict access unless logged in]
def login_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:  
            return redirect(url_for('view.login'))  # Redirect to login page
        return func(*args, **kwargs)
    return decorated_function

# Restrict admin access
def admin_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        user_id = session.get('user_id')
        if user_id is None:
            return redirect(url_for('view.login')) 

        user = User.query.filter_by(userID=user_id).first()
        if user is None or not user.isAdmin:
            abort(403)  # Forbidden access
        return func(*args, **kwargs)
    return decorated_view
