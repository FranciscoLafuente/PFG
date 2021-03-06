# coding=utf-8

from flask import request, jsonify, render_template
from flask_jwt_extended import (jwt_required, fresh_jwt_required, get_jwt_identity, create_access_token, decode_token)
from . import resources
from app.respository import views
import datetime
from app.email import send_email
from app.static import messages as msg
from app.methods import JSONEncoder
import json


@resources.route('/user', methods=['GET'])
def check_user():
    """
    Every time the user changes the page, it checks the token
    :return: The token checked
    """
    token = request.headers['Authorization'].replace('Bearer ', '')
    return jsonify({"access_token": token}), 200


@resources.route('/user/signup', methods=['POST'])
def signup():
    """
    Register a new user
    :return: Successful operation
    """
    req = request.get_json()
    user = req['user']
    is_created = views.UserManagement().create(user)
    if not is_created:
        return jsonify(msg.ALREADY_USE), 400

    return jsonify(msg.SUCCESS), 200


@resources.route('/user/login', methods=['POST'])
def login():
    """
    When the user do login
    :return: The access token
    """
    if not request.is_json:
        return jsonify(msg.MISSING_JSON), 400
    req = request.get_json()['user']

    useremail = req.get('email', None)
    password = req.get('password', None)

    if not useremail or not password:
        return jsonify(msg.MISSING_PARAMETER), 400

    # Verify password and email
    check = views.UserManagement().check(email=useremail, password=password)

    if not check:
        return jsonify(msg.UNREGISTERED), 400

    # Identity can be any data that is json serializable
    expires = datetime.timedelta(days=2)
    access_token = create_access_token(identity=useremail, fresh=True, expires_delta=expires)
    return jsonify(access_token=access_token), 200


@resources.route('/user/forgot', methods=['POST'])
def forgot_password():
    """
    If the user forgot your password
    :return: Successful operation
    """
    url = 'http://localhost:8080/' + 'user/reset/'
    body = request.get_json()
    email = body.get('email')
    if not email:
        return jsonify(msg.MISSING_PARAMETER), 400
    user_email = views.UserManagement().exists(email=email)

    if not user_email:
        return jsonify(msg.NO_DATA), 404
    expires = datetime.timedelta(hours=24)
    reset_token = create_access_token(identity=email, expires_delta=expires)

    send_email('[Shodita] Reset Your Password', sender='shodita@shodita.com', recipients=[email],
               text_body=render_template('email/reset_password.txt', url=url + reset_token),
               html_body=render_template('email/reset_password.html', url=url + reset_token))

    return jsonify(msg.SUCCESS), 200


@resources.route('/user/reset', methods=['POST'])
@jwt_required
def reset_password():
    """
    The user has to introduce a new password
    :return: Successful operation
    """
    body = request.get_json()
    reset_token = body.get('reset_token')
    password = body.get('password')

    if not reset_token or not password:
        return jsonify(msg.MISSING_PARAMETER), 400

    user_email = decode_token(reset_token)['identity']
    is_changed = views.UserManagement().change_password(email=user_email, password=password)
    if not is_changed:
        return jsonify(msg.NO_DATA), 404

    send_email('[Shodita] Password reset successful', sender='shodita@shodita.com', recipients=[user_email],
               text_body='Password reset was successful', html_body='<p>Password reset was successful</p>')

    return jsonify(msg.SUCCESS), 200
