from flask import Blueprint, request, jsonify
from ..model import *
from flask_jwt_extended import jwt_required
from ..utils.decorators import current_user_proxy_obj as current_user


parent = Blueprint('parent', __name__)


@parent.route('/api/get_all_childs')
@jwt_required()
def get_all_childs():
    childs = Parent_Child.query.filter_by(parent_id=current_user().id).all()
    resp = {
        'count': len(childs),
        'childrens': [User.query.filter_by(id=i.user_id).first().as_dict() for i in childs]
    }
    return jsonify(resp)


@parent.route('/api/child_info')
@jwt_required()
def child_info():
    child_id = request.args.get('child_id')
    if Parent_Child.query.filter_by(parent_id=current_user().id).first().user_id != child_id:
        return jsonify(status='error', msg='Parent and child are not related')
    return jsonify(User.query.filter_by(id=child_id).first().as_dict())


@parent.route('/api/get_child_suggestion')
@jwt_required()
def get_child_suggestion():
    cid = Parent_Child.query.filter_by(parent_id=current_user().id).first()
    return jsonify({'data': [i.as_dict() for i in Suggestions.query.filter_by(student_id=cid).all()]})