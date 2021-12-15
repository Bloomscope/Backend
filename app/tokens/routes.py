from flask import Blueprint, jsonify, request
from ..model import *
from ..utils.decorators import current_user_proxy_obj as current_user, admin_required
from flask_jwt_extended import jwt_required


token = Blueprint('token', __name__)


@token.route('/api/get_all_tokens')
@admin_required()
def get_all_tokens():
    all_tokens = Token.query.order_by(Token.created_on.desc()).all()
    resp = {
        'tokens': [i.as_dict() for i in all_tokens]
    }
    return jsonify(resp)


@token.route('/api/get_student_tokens')
@jwt_required()
def get_student_tokens():
    all_tokens = Token.query.filter_by(user_id=current_user().id).order_by(Token.created_on.desc()).all()
    resp = {
        'tokens': [i.as_dict() for i in all_tokens]
    }
    return jsonify(resp)


@token.route('/api/update_token', methods=['POST'])
@admin_required()
def update_token_status():
    data = request.get_json(force=True)
    test_id = data['test_id']
    action = data['action']
    user_id = data['user_id']
    if action not in ['approved', 'rejected']:
        return jsonify({'status': 'error', 'msg': 'invalid action', 'test_id': test_id, 'action': action})
    token = Token.query.filter_by(user_id=user_id).filter_by(test_id=test_id).first()
    token.status = action
    db.session.flush()
    db.session.commit()
    return jsonify(token.as_dict())


@token.route('/api/create_token', methods=['POST'])
@jwt_required()
def create_token():
    data = request.get_json(force=True)
    if Token.query.filter_by(user_id=current_user().id).filter_by(test_id=data['test_id']).first():
        return jsonify({'status': 'error', 'msg': 'token already exists'})
    new_token = Token(**data, user_id=current_user().id)
    db.session.add(new_token)
    db.session.flush()
    db.session.commit()
    return jsonify(token.as_dict())