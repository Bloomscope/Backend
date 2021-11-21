from flask import Blueprint, request, jsonify
from ..utils.decorators import *
from ..model import *


admin_dash = Blueprint('admin_dash', __name__)


@admin_dash.route('/api/get_user_info')
@admin_required()
def get_user_info():
    uid = request.args.get('uid')
    print(uid)
    user = User.query.filter_by(id=uid).first()
    return jsonify(user.as_dict())
