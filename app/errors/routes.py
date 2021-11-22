from flask import jsonify, Blueprint
from werkzeug.exceptions import HTTPException


errors = Blueprint('errors', __name__)


@errors.app_errorhandler(500)
def handle_error(e):
    code = 500
    if isinstance(e, HTTPException):
        code = e.code
    return jsonify(error=str(e)), code


@errors.app_errorhandler(Exception)
def global_error(e):
    error = {
        'error': e.__class__.__name__,
        'msg': e.__str__()
    }
    return jsonify(error), 500