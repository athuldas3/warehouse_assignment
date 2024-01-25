from app.models.user import User
from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
import datetime


def auth_view(request):

    email = request.json.get('email', None)
    password = request.json.get('password', None)
    # fetch user
    user = User.query.filter_by(email=email).first()
    # password check
    if not user:
        return jsonify({"msg": "Invalid username or password"}), 401
    else:
        # password check
        validation_status = User().validate_password(user, password)

        if not validation_status:
            return jsonify({"msg": "Invalid username or password"}), 401
    # Set the expiration time to 7 days from the current time
    expires_delta = datetime.timedelta(days=7)
    access_token = create_access_token(identity=email, expires_delta=expires_delta)
    return jsonify(access_token=access_token), 200
