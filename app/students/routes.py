from flask import Blueprint, request, jsonify
from ..model import *
from flask_jwt_extended import jwt_required
from ..utils.decorators import current_user_proxy_obj as current_user


student = Blueprint('student', __name__)


@student.route('/api/get_announcements')
@jwt_required()
def get_announcements():
    count = request.args.get('count')
    if count is None:
        announcements = Announcements.query.order_by(Announcements.announced_on.desc()).all()
    else:
        announcements = Announcements.query.order_by(Announcements.announced_on.desc()).limit(int(count)).all()
    return jsonify({'count': count,  'announcements': [i.as_dict() for i in announcements]})


@student.route('/api/get_suggestions')
@jwt_required()
def get_suggestions():
    # might have to add student id
    suggestions = Suggestions.query.all()
    return jsonify({'suggestions': [i.as_dict() for i in suggestions]})
