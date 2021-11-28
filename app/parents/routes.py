from flask import Blueprint, request, jsonify
from ..model import *
from flask_jwt_extended import jwt_required
from ..utils.decorators import current_user_proxy_obj as current_user


parent = Blueprint('parent', __name__)
