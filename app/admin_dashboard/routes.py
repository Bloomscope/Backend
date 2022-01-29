from crypt import methods
from flask import Blueprint, request, jsonify
from ..utils.decorators import *
from ..model import *
from ..utils import q_adder, qpicker, mass_reg
import uuid


admin_dash = Blueprint('admin_dash', __name__)


@admin_dash.route('/api/get_user_info')
@admin_required()
def get_user_info():
    uid = request.args.get('uid')
    user = User.query.filter_by(id=uid).first()
    return jsonify(user.as_dict())


@admin_dash.route('/api/get_users')
@admin_required()
def get_users():
    # page = request.args.get('page')
    # datas = User.query.order_by(User.registered_on.desc()).paginate(page=int(1), max_per_page=10, error_out=False)
    datas = User.query.filter(User.user_type_id != 3).order_by(User.registered_on.desc()).paginate(page=1, max_per_page=1000, error_out=False)
    data = {
        'total_pages': datas.pages,
        'has_next_page': datas.has_next,
        'has_previous_page': datas.has_prev,
        'current_page': datas.page,
        'data': [i.as_dict() for i in datas.items]
    }
    return jsonify(data)


@admin_dash.route('/api/get_parent_info')
@admin_required()
def get_parent_info():
    uid = request.args.get('uid')
    if uid is None or not uid:
        pid = Parent_Child.query.filter_by(user_id=uid).first().parent_id
    else:
        pid = Parent_Child.query.filter_by(user_id=current_user_proxy_obj().id).first().parent_id
    parent = Parent.query.filter_by(id=pid).first()
    return jsonify(parent.as_dict())


@admin_dash.route('/api/create_announcement', methods=['POST'])
@admin_required()
def create_announcement():
    data = request.get_json(force=True)
    current_user = current_user_proxy_obj().id
    new_announcement = Announcements(**data, announced_by=current_user)
    db.session.add(new_announcement)
    db.session.flush()
    db.session.commit()
    return jsonify({'status': 'success', 'announcement_id': new_announcement.id, 'id': current_user})


@admin_dash.route('/api/get_announcements')
@admin_required()
def get_all_announcements():
#     count = request.args.get('count')
    count = None
    if count is None:
        announcements = Announcements.query.order_by(Announcements.announced_on.desc()).all()
    else:
        announcements = Announcements.query.order_by(Announcements.announced_on.desc()).limit(int(count)).all()
    return jsonify({'count': count,  'announcements': [i.as_dict() for i in announcements]})


@admin_dash.route('/api/add_suggestions', methods=['POST'])
@admin_required()
def add_suggestions():
    suggestions = request.get_json(force=True)
    new_suggestion = Suggestions(**suggestions)
    db.session.add(new_suggestion)
    db.session.flush()
    db.session.commit()
    return jsonify({'status': 'success', 'suggestion_id': new_suggestion.id, 'to_user': new_suggestion.student_id})


@admin_dash.route('/api/add_questions', methods=['POST'])
@admin_required()
def add_questions():
    # file = request.files['file']
    # q_adder.add_questions(file.read())
    data = request.get_json(force=True)
    q_adder.add_questions(data)
    return jsonify(msg='ok', errors=None)


@admin_dash.route('/api/add_question', methods=['POST'])
@admin_required()
def add_question():
    quest = request.get_json(force=True)
    new_question = Questions(question=quest['question'], options=quest['options'], ans=quest['ans'],\
             marks=quest['marks'], grade=quest['grade'], explanation=quest['explanation'], param_id=quest['param_id'], \
                 added_by_id=current_user_proxy_obj().id)
    db.session.add(new_question)
    db.session.flush()
    db.session.commit()
    return jsonify({'question_id': new_question.id, 'msg': 'success'})


@admin_dash.route('/api/schedule_test', methods=['POST'])
@admin_required()
def schedule_test():
    test_id = uuid.uuid4().__str__()
    data = request.get_json(force=True)
    res = qpicker.get_questions(data['parameters'],grade = data['grade'])
    test_name = data['test_name']
    grades = data['grade']
    duration = int(data['duration']) # in minutes
    conducted_on = int(data['conducted_on'])
    ends_after = int(data['ends_after'])
<<<<<<< HEAD
    new_test = Test(id=test_id, name=test_name, conducted_on=conducted_on, questions=res, durations=duration,\
        grade=data['grade'], ends_on=ends_after)
=======
    new_test = Test(id=test_id, name=test_name, conducted_on=conducted_on, questions=res, durations=duration, ends_on=ends_after,grade = grades)
>>>>>>> 689afb58d083015836765e4384fcc93615d545c1
    db.session.add(new_test)
    db.session.flush()
    db.session.commit()

    return jsonify({'test_id': test_id, 'starts_on': new_test.conducted_on, 'ends_on': new_test.ends_on, \
        'duration': new_test.durations})


@admin_dash.route('/api/get_all_tests')
def get_all_tests():
    tests = Test.query.all()
    del tests['questions']
    resp = {
        'tests': len(tests),
        'data': [i.as_dict() for i in tests]
    }
    return jsonify(resp)


@admin_dash.route('/api/mass_register', methods=['POST'])
@admin_required()
def mass_register():
    # file = request.files['file']
    data = request.get_json(force = True)
    mass_reg.mass_register(data)
    return jsonify(msg='ok')


@admin_dash.route('/api/dashboard')
@admin_required()
def dashboard():
    users = User.query.all()
    tests = Test.query.all()
    grades = Grades.query.all()
    test_data = []
    for grade in grades:
        attempted = TestSchedule.query.filter_by(grade=grade.id).filter_by(has_attempted=True).all()
        total_registered = TestSchedule.query.filter_by(grade=grade.id).all()
        test_data.append({
            "grade": grade.id,
            "attempted": len(attempted),
            "total_registered": len(total_registered)
        })
    resp = {
        "users_registered": len(users),
        "tests": len(tests),
        "test_data": test_data
    }
    return jsonify(resp)


@admin_dash.route('/api/update_access', methods=['POST'])
@admin_required()
def update_access():
    data = request.get_json(force=True)
    resp = {'errors':[]}
    user = User.query.filter_by(id=data['user_id']).first()
    access_level = data['access_level']
    if not user:
        resp['errors'].append(f'User with id {data["user_id"]} does not exist.')
    if access_level > 3 or access_level < 1:
        resp['errors'].append(f'Invalid access level({access_level}) specified')
    else:
        user.user_type_id = int(access_level)
        db.session.commit()
        resp['msg'] = 'User acccess level has been updated'
    return jsonify(resp)


@admin_dash.route('/api/create_organisation', methods=['POST'])
@admin_required()
def create_organisation():
    data = request.get_json(force=True)
    new_org = Organization(name=data['name'], address=['address'])
    db.session.add(new_org)
    db.session.commit()
    return jsonify(msg='ok')