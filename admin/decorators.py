from flask import redirect, url_for, flash
from flask_login import current_user
from functools import wraps

def admin_required(f):
    """Decorador que requiere que el usuario sea admin"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('No tienes permiso para acceder', 'error')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function