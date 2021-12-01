from flask import Blueprint, request, jsonify
from ..utils.decorators import *
from ..model import *


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
    page = request.args.get('page')
    datas = User.query.order_by(User.registered_on.desc()).paginate(page=int(page), max_per_page=10, error_out=False)
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
    pid = Parent_Child.query.filter_by(user_id=uid).first().parent_id
    parent = Parent.query.filter_by(id=pid).first()
    return jsonify(parent.as_dict())


@admin_dash.route('/api/create_announcement', methods=['POST'])
@admin_required()
def create_announcement():
    data = request.get_json(force=True)
    current_user = current_user_proxy_obj()
    new_announcement = Announcements(**data, announced_by=current_user)
    db.session.add(new_announcement)
    db.session.flush()
    db.session.commit()
    return jsonify({'status': 'success', 'announcement_id': new_announcement.id})


@admin_dash.route('/api/get_announcements')
@admin_required()
def get_all_announcements():
    count = request.args.get('count')
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
    return jsonify({'status': 'success', 'suggestion_id': new_suggestion.id})


@admin_dash.route('/api/get_tokens')
@admin_required()
def get_tokens():
    uid = request.args.get('uid')
    resp = {}
    if uid is not None:
        data = Token.query.filter_by(user_id=uid).all()
        resp['data'] = [i.as_dict() for i in data]
    else:
        data = Token.query.all()
        resp['data'] = [i.as_dict() for i in data]
    return jsonify(resp)