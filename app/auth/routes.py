import bcrypt
from flask import Blueprint, request, jsonify, Response, redirect, make_response
from flask.templating import render_template
from flask_jwt_extended.view_decorators import jwt_required
from .. import db, bcrypt
import datetime
from ..model import *
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity


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
        is_parent = user.parent_child_rel
        has_parent = True if len(is_parent) > 0 else False
        parent_id = is_parent[0].parent_id if has_parent else None
        change_pass = True if not user.has_changed_pass else False
        return jsonify({'is_logged_in': True, 'access_token': access_token, \
            'type': user.user_type_id, 'uid': user.id, 'errors': None,\
                'has_parent': has_parent, 'parent_id': parent_id, 'has_default_creds': change_pass})
    user = Parent.query.filter_by(email=data['email']).first()
    if user and bcrypt.check_password_hash(user.password, data['password']):
        access_token = create_access_token(identity=user.email)
        return jsonify({'is_logged_in': True, 'access_token': access_token, 'type': user.user_type_id, 'uid': user.id , 'errors': None})
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
            status['uid'] = user.id
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


@auth.route('/api/update_password', methods=['POST'])
@jwt_required()
def update_pass():
    data = request.get_json(force=True)
    user = User.query.filter_by(email=get_jwt_identity()).first()
    if data['password'] != data['confirm_password']:
        return jsonify(error='Passwords do not match')
    user.password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    user.has_changed_pass = True
    db.session.commit()
    return jsonify(status='success', msg='password has been reset successfully')


@auth.route('/admin_dash_login', methods=['GET', 'POST'])
def admin_dash_login():
    resp = make_response(render_template('admin_login.html'))
    if request.method == 'POST':
        if (request.form
                and request.form['username'] == 'admin'
                and request.form['password'] == 'password'):
                resp.set_cookie('is_logged_in', 'true')
                return redirect('/admin')
        else:
            return Response('Access denied', 403)
    return resp