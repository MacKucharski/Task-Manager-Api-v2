from flask import jsonify
from werkzeug.exceptions import HTTPException, Unauthorized

from api import api
from api.auth import token_auth

@api.errorhandler(HTTPException)
def http_error(error):
    return jsonify({
        "code": error.code,
        "message": error.name,
        "description": error.description
    }), error.code

@token_auth.error_handler
def auth_error():
    raise Unauthorized(description="Authentication failed")