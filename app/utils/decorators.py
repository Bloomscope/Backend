from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request
from flask_jwt_extended import get_jwt_identity
from ..model import User, Parent


def admin_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            user = User.query.filter_by(email=get_jwt_identity()).first()
            if user and user.user_type_id == 3:
                return fn(*args, **kwargs)
            else:
                return jsonify({'error': 'user doesnt have required permission to access route'}), 403
        return decorator
    return wrapper


def current_user_proxy_obj():
    verify_jwt_in_request()
    user = User.query.filter_by(email=get_jwt_identity()).first()
    if user is None:
        user = Parent.query.filter_by(email=get_jwt_identity()).first()
    return user
