from api import api, db
from api.auth import basic_auth, token_auth

@api.route("/tokens", methods=["POST"])
@basic_auth.login_required
def get_token():
    user = basic_auth.current_user()
    token = user.get_token() # type: ignore
    db.session.commit()
    return {"token": token}

@api.route("/tokens", methods=["DELETE"])
@token_auth.login_required
def revoke_token():
    token_auth.current_user().revoke_token() # type: ignore
    db.session.commit()
    return "", 204