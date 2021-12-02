import bcrypt
from flask import Blueprint, request, jsonify
from .. import db, bcrypt
import datetime
from ..model import *
from flask_jwt_extended import create_access_token


auth = Blueprint('auth', __name__)


@auth.route('/api/register_user', methods=['POST'])
def register():
    data = request.get_json(force=True)
    dob = data.pop('dob')
    password = data.pop('password')
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'status': 'failed', 'errors': 'email exists'}), 200
    new_user = User(**data, dob=datetime.datetime.strptime(dob, '%Y-%m-%d'), password=bcrypt.generate_password_hash(password).decode('utf-8'))
    db.session.add(new_user)
    db.session.commit()
    db.session.flush()
    return jsonify({'status': 'success', 'errors': None, 'user_id': new_user.id}), 200


@auth.route('/api/login', methods=['POST'])
def login():
    data = request.get_json(force=True)
    user = User.query.filter_by(email=data['email']).first()
    if user and bcrypt.check_password_hash(user.password, data['password']):
        access_token = create_access_token(identity=user.email)
        return jsonify({'is_logged_in': True, 'access_token': access_token, 'type': user.user_type_id , 'errors': None})
    user = Parent.query.filter_by(email=data['email']).first()
    if user and bcrypt.check_password_hash(user.password, data['password']):
        access_token = create_access_token(identity=user.email)
        return jsonify({'is_logged_in': True, 'access_token': access_token, 'type': user.user_type_id , 'errors': None})
    return jsonify({'is_logged_in': False, 'access_token': None, 'errors': 'email or password doesnt match'})



@auth.route('/api/admin_login', methods=['POST'])
def admin_login():
    data = request.get_json(force=True)
    status = {'is_logged_in': False, 'access_token': None, 'errors': None}
    user = User.query.filter_by(email=data['email']).first()
    if user and bcrypt.check_password_hash(user.password, data['password']):
        if user.user_type_id == 3:
            access_token = create_access_token(identity=user.email)
            status['is_logged_in'] = True
            status['access_token'] = access_token
            status['type'] = 3
            return jsonify(status), 200
        else:
            status['errors'] = 'user doesnt have permission to acces this routes'
            return jsonify(status), 403
    status['errors'] = 'email or password doesnt match'
    return jsonify(status), 401


@auth.route('/api/register_parent', methods=['POST'])
def register_parent():
    data = request.get_json(force=True)
    uid = data.pop('uid')
    dob = data.pop('dob')
    password = data.pop('password')
    user = User.query.filter_by(id=uid).first()
    if user:
        new_parent = Parent(**data, dob=datetime.datetime.strptime(dob, '%Y-%m-%d'), password=bcrypt.generate_password_hash(password).decode('utf-8'))
        db.session.add(new_parent)
        db.session.flush()
        new_relation = Parent_Child(parent_id=new_parent.id, user_id=uid)
        db.session.add(new_relation)
        db.session.commit()
        return jsonify({'status': 'success', 'errors': None})
    return jsonify({'status': 'failed', 'errors': 'user not found'})
