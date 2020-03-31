# coding=utf-8

from flask import request, jsonify
from flask_jwt_extended import (JWTManager, jwt_required, fresh_jwt_required, create_access_token, get_jwt_identity,
                                decode_token)
from . import main
from ..models import *
import datetime
import jwt


# USERS MANAGEMENT

@main.route('/signup', methods=['POST'])
def signup():
    new_user = User()
    new_user.insert(request.json)

    return jsonify({"msg": "Success!"}), 200


@main.route('/login', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    useremail = request.json.get('email', None)
    password = request.json.get('password', None)

    if not useremail or not password:
        return jsonify({"msg": "Missing parameter"}), 400

    # Verify password and email
    user = User()
    check = user.check_user(request.json)

    if check is False:
        return jsonify({"msg": "Unregistered user or invalid password"}), 400

    # Identity can be any data that is json serializable
    expires = datetime.timedelta(seconds=10)
    access_token = create_access_token(identity=useremail, fresh=True, expires_delta=expires)
    return jsonify(access_token=access_token), 200


@main.route('/forgot', methods=['POST'])
def forgot_password():
    url = 'http://localhost:8080/' + 'reset/'
    body = request.get_json()
    email = body.get('email')
    if not email:
        return jsonify({"msg": "Missing parameter"}), 400
    user = User()
    user_email = user.get_user(email)
    if not user_email:
        return jsonify({"msg": "User not found"}), 404
    expires = datetime.timedelta(hours=24)
    reset_token = create_access_token(identity=email, expires_delta=expires)

    send_email('[Shodita] Reset Your Password', sender='shodita@shodita.com', recipients=[email],
               text_body=render_template('email/reset_password.txt', url=url + reset_token),
               html_body=render_template('email/reset_password.html', url=url + reset_token))

    return jsonify({"msg": "Success!"}), 200


@main.route('/reset', methods=['POST'])
@jwt_required
def reset_password():
    body = request.get_json()
    reset_token = body.get('reset_token')
    password = body.get('password')

    if not reset_token or not password:
        return jsonify({"msg": "Missing parameter"}), 400

    user_email = decode_token(reset_token)['identity']
    u = User()
    new_user = u.change_password(user_email, password)
    if new_user is None:
        return jsonify({"msg": "User not found"}), 404

    send_email('[Shodita] Password reset successful', sender='shodita@shodita.com', recipients=[user_email],
               text_body='Password reset was successful', html_body='<p>Password reset was successful</p>')

    return jsonify({"msg": "Success!"}), 200


@main.route('/myprofile', methods=['GET'])
@fresh_jwt_required
def get_user():
    current_user = get_jwt_identity()
    u = User()

    return jsonify(u.get_user(current_user)), 200


# MY PROJECT MANAGEMENT

@main.route('/myproject', methods=['GET'])
@fresh_jwt_required
def get_products():
    current_user = get_jwt_identity()
    project_user = Project()
    all_projects = project_user.project_with_scans(current_user)

    return jsonify(all_projects), 200


@main.route('/myproject', methods=['POST'])
@fresh_jwt_required
def post_products():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    project_name = request.json.get('name', None)
    project_type = request.json.get('type', None)

    if not project_name or not project_type:
        return jsonify({"msg": "Missing parameter"}), 400

    current_user = get_jwt_identity()
    project_user = Project()
    p = project_user.create_projetc(current_user, project_name, project_type)

    return jsonify(p), 200


@main.route('/myproject/<id>', methods=['POST'])
@fresh_jwt_required
def scans(id):
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    scan_name = request.json.get('name', None)
    scan_bots = request.json.get('bots', None)
    scan_hosts = request.json.get('hosts', None)
    scan_executiontime = request.json.get('executiontime', None)

    if not scan_name or not scan_bots or not scan_hosts or not scan_executiontime:
        return jsonify({"msg": "Missing parameter"}), 400

    current_user = get_jwt_identity()
    s = Scan()
    new_scan = s.create_scan(current_user, id, scan_name, scan_bots, scan_hosts, scan_executiontime)

    return jsonify(new_scan), 200


@main.route('/myproject/<id>', methods=['DELETE'])
@fresh_jwt_required
def delete_project(id):
    current_user = get_jwt_identity()
    if id is not None:
        p = Project()
        is_delete = p.delete_project(id, current_user)
        if is_delete:
            return jsonify({"msg": "Success!"}), 200
    return jsonify({"msg": "Project not found"}), 404


# BOTS MANAGEMENT

@main.route('/bots', methods=['GET'])
@fresh_jwt_required
def get_bots():
    current_user = get_jwt_identity()
    b = Bot()
    list_bots = b.get_bots(current_user)

    return jsonify(list_bots), 200


@main.route('/bots', methods=['POST'])
@fresh_jwt_required
def post_bots():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    bot_name = request.json.get('name', None)
    bot_ip = request.json.get('ip', None)
    bot_type = request.json.get('type', None)

    if not bot_name or not bot_ip or not bot_type:
        return jsonify({"msg": "Missing parameter"}), 400

    current_user = get_jwt_identity()
    b = Bot()
    bot = b.create_bot(bot_name, current_user, bot_ip, bot_type)

    return jsonify(bot), 200


@main.route('/bots/<id_bot>', methods=['GET'])
@fresh_jwt_required
def generate_token_bot(id_bot):
    token_bot = create_access_token(identity=id_bot, expires_delta=False)
    b = Bot()
    bot_update = b.add_token(id_bot, token_bot)

    return jsonify(token_bot, bot_update), 200


@main.route('/bots/<id_bot>', methods=['DELETE'])
@fresh_jwt_required
def delete_bot(id_bot):
    if id_bot is not None:
        b = Bot()
        is_delete = b.delete_bot(id_bot)
        if is_delete:
            return jsonify({"msg": "Success!"}), 200
    return jsonify({"msg": "Bot not found"}), 404


# CONNECT WITH BOTS (CEMENT)

@main.route('/bots/login', methods=['POST'])
@jwt_required
def login_bots():
    bot_ip = request.remote_addr
    bot_id = get_jwt_identity()
    # Search if the bot exists in database
    b = Bot()
    type_bot = b.search_bot(bot_ip, bot_id)
    if type_bot is None:
        return jsonify({"msg": "Unregistered bot"}), 400

    expires = datetime.timedelta(days=2)
    token_bot = create_access_token(identity=bot_id, fresh=True, expires_delta=expires,
                                    user_claims=type_bot)

    return jsonify(token_bot), 200


@main.route('/bots/scans', methods=['GET'])
@fresh_jwt_required
def scans_by_bot():
    bot_id = get_jwt_identity()
    s = Scan()
    bot_scans = s.get_scans_by_bot(bot_id)

    return jsonify(bot_scans), 200


@main.route('/bots/nobita/<scan_id>', methods=['POST'])
@fresh_jwt_required
def save_nobita(scan_id):
    scan = request.json
    n = Nobita()
    result = n.save_scan(scan)
    if result is not None:
        s = Scan()
        s.change_done(scan_id)
    return jsonify({"msg": "Success!"}), 200


@main.route('/bots/shizuka', methods=['POST'])
@fresh_jwt_required
def save_shizuka():
    data = request.json
    sh = Shizuka()
    sh.save_ipreverse(data)
    return jsonify({"msg": "Success!"}), 200


@main.route('/bots/suneo', methods=['POST'])
@fresh_jwt_required
def save_suneo():
    data = request.json
    if data:
        su = Suneo()
        su.save_domain(data)
        return jsonify({"msg": "Success!"}), 200
    return jsonify({"msg": "The received data is empty"}), 400


@main.route('/bots/gigante', methods=['POST'])
@fresh_jwt_required
def save_gigante():
    data = request.json
    if data:
        gi = Gigante()
        gi.save_ssh(data)
        return jsonify({"msg": "Success!"}), 200
    return jsonify({"msg": "The received data is empty"}), 400
