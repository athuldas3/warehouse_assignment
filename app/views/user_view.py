from flask import jsonify
from app.models.user import User
from app.one_time_scripts.user_scripts import UserScripts


def create_dummy_users():
    users = User.query.all()
    if not users:
        UserScripts().create_user()
        users = User.query.all()
    user_list = [{'username': user.username, 'email': user.email} for user in users]
    return jsonify(user_list)
