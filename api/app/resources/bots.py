# coding=utf-8

from flask import request, jsonify
from flask_jwt_extended import (jwt_required, fresh_jwt_required, create_access_token, get_jwt_identity)
from . import resources
from app.models import Bot, Scan, Nobita, Suneo, Shizuka, Gigante
from app.respository import views
import datetime


@resources.route('/bots', methods=['GET'])
@fresh_jwt_required
def get_bots():
    current_user = get_jwt_identity()
    list_bots = views.BotManagement().get_bots(email=current_user)

    return jsonify(list_bots), 200


@resources.route('/bots', methods=['POST'])
@fresh_jwt_required
def create_bots():
    current_user = get_jwt_identity()
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    bot_name = request.json.get('name', None)
    bot_ip = request.json.get('ip', None)
    bot_type = request.json.get('type', None)

    if not bot_name or not bot_ip or not bot_type:
        return jsonify({"msg": "Missing parameter"}), 400

    bot = views.BotManagement().create(name=bot_name, email=current_user, ip=bot_ip, type=bot_type)

    return jsonify(bot), 200


@resources.route('/bots/<id_bot>', methods=['GET'])
@fresh_jwt_required
def generate_token_bot(id_bot):
    token_bot = create_access_token(identity=id_bot, expires_delta=False)
    views.BotManagement().add_token(id=id_bot, token=token_bot)

    return jsonify(token_bot), 200


@resources.route('/bots/<id_bot>', methods=['DELETE'])
@fresh_jwt_required
def delete_bot(id_bot):
    if id_bot:
        views.BotManagement().delete(id=id_bot)
        return jsonify({"msg": "Success!"}), 200
    return jsonify({"msg": "Bot not found"}), 404


# CONNECT WITH BOTS (CEMENT)

@resources.route('/bots/login', methods=['POST'])
@jwt_required
def login_bots():
    bot_ip = request.remote_addr
    bot_id = get_jwt_identity()
    # Search if the bot exists in database
    type_bot = views.BotManagement().search_bot(id=bot_id, ip=bot_ip)
    if not type_bot:
        return jsonify({"msg": "Unregistered bot"}), 400

    expires = datetime.timedelta(days=2)
    token_bot = create_access_token(identity=bot_id, fresh=True, expires_delta=expires,
                                    user_claims=type_bot)

    return jsonify(token_bot), 200


@resources.route('/bots/scans', methods=['GET'])
@fresh_jwt_required
def scans_by_bot():
    bot_id = get_jwt_identity()
    bot_scans = views.ScanManagement().scans_by_bot(bot=bot_id)

    return jsonify(bot_scans), 200


@resources.route('/bots/nobita', methods=['POST'])
@fresh_jwt_required
def save_nobita():
    data = request.json
    if not data:
        return jsonify({"msg": "The received data is empty"}), 400
    for d in data:
        views.NobitaManagement().create(data=d)

    return jsonify({"msg": "Success!"}), 200


@resources.route('/bots/shizuka', methods=['POST'])
@fresh_jwt_required
def save_shizuka():
    data = request.json
    if not data:
        return jsonify({"msg": "The received data is empty"}), 400
    for d in data:
        views.ShizukaManagement().create(data=d)

    return jsonify({"msg": "Success!"}), 200


@resources.route('/bots/suneo', methods=['POST'])
@fresh_jwt_required
def save_suneo():
    data = request.json
    if not data:
        return jsonify({"msg": "The received data is empty"}), 400
    views.SuneoManagement().create(data=data)

    return jsonify({"msg": "Success!"}), 200


@resources.route('/bots/gigante', methods=['POST'])
@fresh_jwt_required
def save_gigante():
    data = request.json
    if not data:
        return jsonify({"msg": "The received data is empty"}), 400
    views.GiganteManagement().create(data=data)

    return jsonify({"msg": "Success!"}), 200


@resources.route('/bots/update_done/<scan_id>', methods=['PUT'])
@fresh_jwt_required
def update_done(scan_id):
    views.ScanManagement().change_done(id=scan_id, value=True)
    return jsonify({"msg": "Success!"}), 200
