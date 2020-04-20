# coding=utf-8

from flask import request, jsonify, render_template
from flask_jwt_extended import (jwt_required, fresh_jwt_required, get_jwt_identity, create_access_token, decode_token)
from . import resources
from app.respository import views
import datetime
from app.email import send_email


@resources.route('/user', methods=['GET'])
@fresh_jwt_required
def check_user():
    token = request.headers['Authorization'].replace('Bearer ', '')
    return jsonify({"access_token": token}), 200


@resources.route('/signup', methods=['POST'])
def signup():
    user = views.UserManagement().create(request.json)
    if not user:
        return jsonify({"msg": "The email is alredy in use"}), 400

    return jsonify({"msg": "Success!"}), 200


@resources.route('/login', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400
    req = request.get_json()['user']

    useremail = req.get('email', None)
    password = req.get('password', None)

    if not useremail or not password:
        return jsonify({"msg": "Missing parameter"}), 400

    # Verify password and email
    check = views.UserManagement().check(email=useremail, password=password)

    if not check:
        return jsonify({"msg": "Unregistered user or invalid password"}), 400

    # Identity can be any data that is json serializable
    expires = datetime.timedelta(days=2)
    access_token = create_access_token(identity=useremail, fresh=True, expires_delta=expires)
    return jsonify(access_token=access_token), 200


@resources.route('/forgot', methods=['POST'])
def forgot_password():
    url = 'http://localhost:8080/' + 'reset/'
    body = request.get_json()
    email = body.get('email')
    if not email:
        return jsonify({"msg": "Missing parameter"}), 400
    user_email = views.UserManagement().exists(email=email)

    if not user_email:
        return jsonify({"msg": "User not found"}), 404
    expires = datetime.timedelta(hours=24)
    reset_token = create_access_token(identity=email, expires_delta=expires)

    send_email('[Shodita] Reset Your Password', sender='shodita@shodita.com', recipients=[email],
               text_body=render_template('email/reset_password.txt', url=url + reset_token),
               html_body=render_template('email/reset_password.html', url=url + reset_token))

    return jsonify({"msg": "Success!"}), 200


@resources.route('/reset', methods=['POST'])
@jwt_required
def reset_password():
    body = request.get_json()
    reset_token = body.get('reset_token')
    password = body.get('password')

    if not reset_token or not password:
        return jsonify({"msg": "Missing parameter"}), 400

    user_email = decode_token(reset_token)['identity']
    is_changed = views.UserManagement().change_password(email=user_email, password=password)
    if not is_changed:
        return jsonify({"msg": "User not found"}), 404

    send_email('[Shodita] Password reset successful', sender='shodita@shodita.com', recipients=[user_email],
               text_body='Password reset was successful', html_body='<p>Password reset was successful</p>')

    return jsonify({"msg": "Success!"}), 200


@resources.route('/myprofile', methods=['GET'])
@fresh_jwt_required
def get_user():
    pass
