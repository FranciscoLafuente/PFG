# coding=utf-8

from flask import request, jsonify
from flask_jwt_extended import (jwt_required, fresh_jwt_required, create_access_token, get_jwt_identity)
from . import resources
from app.respository import views
from app.respository import generic_model
import datetime
from app.static import messages as msg
from pprint import pprint


@resources.route('/bots', methods=['GET'])
@fresh_jwt_required
def get_bots():
    current_user = get_jwt_identity()
    list_bots = views.MyBotsManagement().get_bots(email=current_user)

    return jsonify(list_bots), 200


@resources.route('/bots', methods=['POST'])
@fresh_jwt_required
def create_bots():
    current_user = get_jwt_identity()
    if not request.is_json:
        return jsonify(msg.MISSING_JSON), 400

    bot_name = request.json.get('name', None)
    bot_ip = request.json.get('ip', None)
    bot_type = request.json.get('type', None)

    if not bot_name or not bot_ip or not bot_type:
        return jsonify(msg.MISSING_PARAMETER), 400

    bot = views.MyBotsManagement().create(name=bot_name, email=current_user, ip=bot_ip, type=bot_type)
    if not bot:
        return jsonify(msg.ALREADY_USE), 400

    return jsonify(bot), 200


@resources.route('/bots/<id_bot>', methods=['GET'])
@fresh_jwt_required
def generate_token_bot(id_bot):
    token_bot = create_access_token(identity=id_bot, expires_delta=False)
    views.MyBotsManagement().add_token(id=id_bot, token=token_bot)

    return jsonify(token_bot), 200


@resources.route('/bots/<id_bot>', methods=['PUT'])
@fresh_jwt_required
def renew_token_bot(id_bot):
    token_bot = create_access_token(identity=id_bot, expires_delta=False)
    views.MyBotsManagement().add_token(id=id_bot, token=token_bot)

    return jsonify(token_bot), 200


@resources.route('/bots/<id_bot>', methods=['DELETE'])
@fresh_jwt_required
def delete_bot(id_bot):
    if id_bot:
        views.MyBotsManagement().delete(id=id_bot)
        return jsonify(msg.SUCCESS), 200
    return jsonify(msg.NO_DATA), 404


# CONNECT WITH BOTS (CEMENT)

@resources.route('/bots/tokens', methods=['GET'])
def get_token_bots():
    bots = views.MyBotsManagement().get_all_bots()
    return jsonify(bots)


@resources.route('/bots/login', methods=['POST'])
@jwt_required
def login_bot():
    bot_ip = request.remote_addr
    bot_id = get_jwt_identity()
    # Search if the bot exists in database
    type_bot = views.MyBotsManagement().search_bot(id=bot_id, ip=bot_ip)
    if not type_bot:
        return jsonify(msg.UNREGISTERED), 400

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


@resources.route('/bots/data/<id_scan>/<domain>', methods=['POST'])
@fresh_jwt_required
def save_data(id_scan, domain):
    data = request.json
    if not data:
        return jsonify(msg.NO_DATA), 400

    db_id = views.ScansDataManagement().create(scan=id_scan, domain=domain)
    for item in data:
        if not item:
            return jsonify(msg.SUCCESS), 200
        bot_name = item['bot']
        id = generic_model.Generic().create(name=bot_name, data=item)
        if id:
            # Save data in a dict
            scan = {bot_name: id}
            views.ScansDataManagement().store_results(id=db_id, list=scan)

    return jsonify(msg.SUCCESS), 200


@resources.route('/bots/nobita', methods=['POST'])
@fresh_jwt_required
def save_nobita():
    data = request.json
    if not data:
        return jsonify(msg.NO_DATA), 400
    for d in data:
        views.NobitaManagement().create(data=d)

    return jsonify(msg.SUCCESS), 200


@resources.route('/bots/shizuka', methods=['POST'])
@fresh_jwt_required
def save_shizuka():
    data = request.json
    if not data:
        return jsonify(msg.NO_DATA), 400
    for d in data:
        views.ShizukaManagement().create(data=d)

    return jsonify(msg.SUCCESS), 200


@resources.route('/bots/suneo', methods=['POST'])
@fresh_jwt_required
def save_suneo():
    data = request.json
    if not data:
        return jsonify(msg.NO_DATA), 400
    views.SuneoManagement().create(data=data)

    return jsonify(msg.SUCCESS), 200


@resources.route('/bots/gigante', methods=['POST'])
@fresh_jwt_required
def save_gigante():
    data = request.json
    if not data:
        return jsonify(msg.NO_DATA), 400
    views.GiganteManagement().create(data=data)

    return jsonify(msg.SUCCESS), 200


@resources.route('/bots/update_done/<scan_id>', methods=['PUT'])
@fresh_jwt_required
def update_done(scan_id):
    views.ScanManagement().change_done(id=scan_id, value=True)
    return jsonify(msg.SUCCESS), 200
