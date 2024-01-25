from app import app
from app.custom_decorators.check_required_fields import check_required_fields
from app.views.auth_view import auth_view
from flask import Flask, jsonify, request


@app.route('/user/login', methods=['POST'])
@check_required_fields(['email', 'password'])
def login():
    return auth_view(request)
