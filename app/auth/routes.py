import bcrypt
from flask import Blueprint, request, jsonify
from .. import db, bcrypt, jwt
import datetime
from ..model import *
from flask_jwt_extended import create_access_token


auth = Blueprint('auth', __name__)


@auth.route('/api/register', methods=['POST'])
def register():
    data = request.get_json(force=True)
    dob = data.pop('dob')
    password = data.pop('password')
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'status': 'failed', 'errors': 'email exists'}), 200
    new_user = User(**data, dob=datetime.datetime.strptime(dob, '%Y-%m-%d'), password=bcrypt.generate_password_hash(password).decode('utf-8'))
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'status': 'success', 'errors': None}), 200


@auth.route('/api/login', methods=['POST'])
def login():
    data = request.get_json(force=True)
    user = User.query.filter_by(email=data['email']).first()
    if user and bcrypt.check_password_hash(user.password, data['password']):
        access_token = create_access_token(identity=user.email)
        return jsonify({'is_logged_in': True, 'access_token': access_token, 'errors': None})
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
            return jsonify(status)
        else:
            status['errors'] = 'user doesnt have permission to acces this routes'
            return jsonify(status)
    status['errors'] = 'email or password doesnt match'
    return jsonify(status)