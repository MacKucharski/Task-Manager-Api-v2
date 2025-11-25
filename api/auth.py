import sqlalchemy as sa
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth

from api import db
from api.models import User

basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth()

@basic_auth.verify_password
def verify_password(email, password):
    query = sa.select(User).where(User.email == email)
    user = db.session.scalar(query)
    if user and user.password_hash == password:
        return user

@token_auth.verify_token
def verify_token(token):
    return User.check_token(token) if token else None

    