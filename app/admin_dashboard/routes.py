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


@admin_dash.route('/api/create_announcement')
@admin_required()
def create_announcement():
    data = request.get_json(force=True)
    new_announcement = Announcements(**data)
    db.session.add(new_announcement)
    db.session.flush()
    db.session.commit()
    return jsonify({'status': 'success', 'announcement_id': new_announcement.id})