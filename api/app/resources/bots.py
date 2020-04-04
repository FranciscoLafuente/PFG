# coding=utf-8

from flask import request, jsonify
from flask_jwt_extended import (jwt_required, fresh_jwt_required, create_access_token, get_jwt_identity)
from . import resources
from app.models import Bot, Scan, Nobita, Suneo, Shizuka, Gigante
import datetime


@resources.route('/bots', methods=['GET'])
@fresh_jwt_required
def get_bots():
    current_user = get_jwt_identity()
    b = Bot()
    list_bots = b.get_bots(current_user)

    return jsonify(list_bots), 200


@resources.route('/bots', methods=['POST'])
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


@resources.route('/bots/<id_bot>', methods=['GET'])
@fresh_jwt_required
def generate_token_bot(id_bot):
    token_bot = create_access_token(identity=id_bot, expires_delta=False)
    b = Bot()
    bot_update = b.add_token(id_bot, token_bot)

    return jsonify(token_bot, bot_update), 200


@resources.route('/bots/<id_bot>', methods=['DELETE'])
@fresh_jwt_required
def delete_bot(id_bot):
    if id_bot is not None:
        b = Bot()
        is_delete = b.delete_bot(id_bot)
        if is_delete:
            return jsonify({"msg": "Success!"}), 200
    return jsonify({"msg": "Bot not found"}), 404


# CONNECT WITH BOTS (CEMENT)

@resources.route('/bots/login', methods=['POST'])
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


@resources.route('/bots/scans', methods=['GET'])
@fresh_jwt_required
def scans_by_bot():
    bot_id = get_jwt_identity()
    s = Scan()
    bot_scans = s.get_scans_by_bot(bot_id)

    return jsonify(bot_scans), 200


@resources.route('/bots/nobita', methods=['POST'])
@fresh_jwt_required
def save_nobita():
    scan = request.json
    n = Nobita()
    result = n.save_scan(scan)
    if result is None:
        jsonify({"msg": "The scan hasn't been saved"}), 400
    return jsonify({"msg": "Success!"}), 200


@resources.route('/bots/shizuka', methods=['POST'])
@fresh_jwt_required
def save_shizuka():
    data = request.json
    sh = Shizuka()
    sh.save_ipreverse(data)
    return jsonify({"msg": "Success!"}), 200


@resources.route('/bots/suneo', methods=['POST'])
@fresh_jwt_required
def save_suneo():
    data = request.json
    if data:
        su = Suneo()
        su.save_domain(data)
        return jsonify({"msg": "Success!"}), 200
    return jsonify({"msg": "The received data is empty"}), 400


@resources.route('/bots/gigante', methods=['POST'])
@fresh_jwt_required
def save_gigante():
    data = request.json
    if data:
        gi = Gigante()
        gi.save_ssh(data)
        return jsonify({"msg": "Success!"}), 200
    return jsonify({"msg": "The received data is empty"}), 400


@resources.route('/bots/update_done/<scan_id>', methods=['PUT'])
@fresh_jwt_required
def update_done(scan_id):
    s = Scan()
    update = s.change_done(scan_id, True)
    if update is None:
        return jsonify({"msg": "Scan not found"}), 404
    return jsonify({"msg": "Success!"}), 200
