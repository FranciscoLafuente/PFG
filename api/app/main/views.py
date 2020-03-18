# coding=utf-8

from flask import request, jsonify
from flask_jwt_extended import (JWTManager, jwt_required, create_access_token, get_jwt_identity)
from . import main
from ..models import User, Project, Scan, Bot
import datetime


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
    access_token = create_access_token(identity=useremail, expires_delta=None)
    return jsonify(access_token=access_token), 200


@main.route('/myprofile', methods=['GET'])
@jwt_required
def get_user():
    current_user = get_jwt_identity()
    u = User()

    return jsonify(u.get_user(current_user)), 200


@main.route('/myproject', methods=['GET'])
@jwt_required
def get_products():
    current_user = get_jwt_identity()
    project_user = Project()
    all_projects = project_user.project_with_scans(current_user)

    return jsonify(all_projects), 200


@main.route('/myproject', methods=['POST'])
@jwt_required
def post_products():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    project_name = request.json.get('name', None)
    project_type = request.json.get('type', None)

    if not project_name or not project_type:
        return jsonify({"msg": "Missing parameter"}), 400

    current_user = get_jwt_identity()
    project_user = Project()
    project_user.create_projetc(current_user, project_name, project_type)

    return jsonify({"msg": "Success!"}), 200


@main.route('/myproject/<id>', methods=['POST'])
@jwt_required
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
    s.create_scan(current_user, id, scan_name, scan_bots, scan_hosts, scan_executiontime)

    # Return all projects update
    project_user = Project()
    all_projects = project_user.project_with_scans(current_user)

    return jsonify(all_projects), 200


@main.route('/bots', methods=['GET'])
@jwt_required
def get_bots():
    current_user = get_jwt_identity()
    b = Bot()
    list_bots = b.get_bots(current_user)

    return jsonify(list_bots), 200


@main.route('/bots', methods=['POST'])
@jwt_required
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
    id_bot = b.create_bot(bot_name, current_user, bot_ip, bot_type)

    return jsonify(id_bot), 200


@main.route('/bots/<id_bot>', methods=['GET'])
@jwt_required
def generate_token_bot(id_bot):
    token_bot = create_access_token(identity=id_bot, expires_delta=False)
    b = Bot()
    bot_update = b.add_token(id_bot, token_bot)

    return jsonify(token_bot, bot_update), 200


# CONNECT WITH CEMENT

@main.route('/bots/<user>', methods=['GET'])
@jwt_required
def bots_by_user(user):
    b = Bot()
    list_bots = b.get_bots(user)

    return jsonify(list_bots), 200


@main.route('/myproject/<user>', methods=['GET'])
@jwt_required
def products_by_user(user):
    project_user = Project()
    all_projects = project_user.project_with_scans(user)

    return jsonify(all_projects), 200


@main.route('/bots/login', methods=['POST'])
@jwt_required
def login_bots():
    bot_ip = request.remote_addr
    bot_token = request.headers.get('Authorization').lstrip('Bearer ')
    # Search if the bot exists in database
    b = Bot()
    b.search_bot(bot_ip, bot_token)
    # TODO: la ip tiene que coincidir con la ip que tenemos en base de datos, dentro del bot correspondiente. Hay que
    #  obtener el tipo de bot y su id, para introducirlo en el token. identity=idbot
    expires = datetime.timedelta(days=2)
    token_bot = create_access_token(bot_ip, expires_delta=expires)

    return jsonify(), 200
