from flask import Blueprint, request, jsonify
from ..model import *
from flask_jwt_extended import jwt_required
from ..utils.decorators import current_user_proxy_obj as current_user


student = Blueprint('student', __name__)


@student.route('/api/user_get_announcements')
@jwt_required()
def get_announcements():
    count = request.args.get('count')
    if count is None:
        announcements = Announcements.query.order_by(Announcements.announced_on.desc()).all()
    else:
        announcements = Announcements.query.order_by(Announcements.announced_on.desc()).limit(int(count)).all()
    return jsonify({'count': count,  'announcements': [i.as_dict() for i in announcements]})


@student.route('/api/student_info')
@jwt_required()
def student_info():
    user = User.query.filter_by(id=current_user().id).first()
    return jsonify(user.as_dict())


@student.route('/api/get_suggestions')
@jwt_required()
def get_suggestions():
    uid = request.args.get('id')
    if uid is None or uid == '':
        return jsonify({'user_id': uid, 'errors': 'invalid user id or invalid session'})
    suggestions = Suggestions.query.filter_by(user_id=uid).all()
    return jsonify({'user_id': uid, 'suggestions': [i.as_dict() for i in suggestions]})


@student.route('/api/create_token', methods=['POST'])
@jwt_required()
def new_token():
    data = request.get_json(force=True)
    new_token = Token(**data, user_id=current_user().id)
    db.session.add(new_token)
    db.session.flush()
    db.session.commit()
    return jsonify({'errors': None, 'status': 'success', 'id': new_token.id})


@student.route('/api/get_report')
@jwt_required()
def get_report():
    tests = Test.query.all()
    tests_lists = [(i.id, i.name) for i in tests]
    res = {'data': []}
    for i in tests_lists:
        has_attempted = TestAttempts.query.filter_by(user_id=current_user().id).filter_by(test_id=i[0]).first() is not None
        if has_attempted:
            res['data'].append({'test_id': i[0], 'test_name': i[1], 'user_id': current_user().id, 'has_attempted': True})
        else:
            res['data'].append({'test_id': i[0], 'test_name': i[1], 'user_id': current_user().id, 'has_attempted': False})
    return jsonify(res)
