from functools import wraps

from flask import abort,redirect, url_for
from flask_login import current_user, AnonymousUserMixin

from .models import ConsensusTask


def permission_required(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if current_user.is_anonymous:
                return redirect(url_for('main.index'))
            if not current_user.pode(permissao=permission):
               abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def admin_required(f):
    return permission_required(ConsensusTask.ADMINISTRAR_SISTEMA)(f)