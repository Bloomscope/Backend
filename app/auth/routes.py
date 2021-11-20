from flask import Blueprint, request, jsonify
from .. import db
import datetime
from ..model import *


auth = Blueprint('auth', __name__)


@auth.route('/api/register', methods=['POST'])
def register():
    data = request.get_json(force=True)
    dob = data.pop('dob')
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'status': 'failed', 'error': 'email exists'}), 200
    new_user = User(**data, dob=datetime.datetime.strptime(dob, '%Y-%m-%d'))
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'status': 'success'}), 200


@auth.route('/api/login', methods=['POST'])
def login():
    data = request.get_json(force=True)
    user = User.query.filter_by(email=data['email']).first()
    if user and user.password == 
