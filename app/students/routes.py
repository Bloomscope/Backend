from flask import Blueprint, request, jsonify
from ..model import *
from flask_jwt_extended import jwt_required
from ..utils.decorators import current_user_proxy_obj as current_user
from datetime import datetime
from ..utils import evaluator


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
    uid =current_user().id
    suggestions = Suggestions.query.filter_by(student_id=uid).all()
    return jsonify({'user_id': uid, 'suggestions': [i.as_dict() for i in suggestions]})


@student.route('/api/get_tests')
@jwt_required()
def get_tests():
    tests = TestSchedule.query.filter_by(user_id=current_user().id).all()
    print(tests)
    resp = {'data': []}
    for test in tests:
        data = test.as_dict()
        if datetime.utcnow() > test.starts_on or datetime.utcnow() > test.ends_on:
            data['date'] = 0
        if datetime.utcnow() < test.starts_on:
            data['date'] = -1
        if datetime.utcnow() > test.ends_on:
            data['date'] = 1
        data['name'] = Test.query.filter_by(id=test.test_id).first().name
        resp['data'].append(data)
    return jsonify(resp)


@student.route('/api/test_info')
@jwt_required()
def test_info():
    test_id = request.args.get('test_id')
    test = Test.query.filter_by(id=test_id).first()
    test = test.as_dict()
    del test['questions']
    return jsonify(test)


@student.route('/api/eval_test', methods=['POST'])
@jwt_required()
def eval_test():
    data = request.get_json(force=True)
    resp = evaluator.Eval(data).evaluate()
    return jsonify(resp)


@student.route('/api/get_results')
@jwt_required()
def get_results():
    results = Results.query.filter_by(user_id=current_user().id).all()
    resp = {'results': [i.as_dict() for i in results]}
    return jsonify(resp)


@student.route('/api/get_result')
@jwt_required()
def get_result():
    test_id = request.args.get('test_id')
    if test_id is None:
        return jsonify(errors='test_id not given')
    result = Results.query.filter_by(test_id=test_id).filter_by(user_id=current_user().id).first()
    return jsonify(result.as_dict())


@student.route('/api/quiz', methods=['POST'])
@jwt_required()
def quiz():
    data = request.get_json(force=True)
    test = Test.query.filter_by(id=data['test_id']).first()
    checks = TestSchedule.query.filter_by(user_id=current_user().id).filter_by(test_id=data['test_id']).first()
    if not checks:
        return jsonify(error = 'No test schedules found for the user.')
    if checks.has_attempted:
        return jsonify(error = 'user has already taken the test.')
    resp = {
        'test_id': test.id,
        'questions': test.questions,
        'duration': test.durations
    }
    return jsonify(resp)
