# coding=utf-8

from flask import request, jsonify, send_from_directory
from flask_jwt_extended import (jwt_required, fresh_jwt_required, create_access_token, get_jwt_identity)
from flask import current_app as app
from werkzeug.utils import secure_filename
from . import resources
from app.respository import views
from app.respository import generic_model
import datetime
from app.static import messages as msg
from pprint import pprint
import os
from os import listdir
from os.path import isfile, join


def allowed_file(filename):
    """
    File extension allowed to upload bot files
    :param filename: File you want to upload
    :return: If it's allowed, return True
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


@resources.route('/mybots', methods=['GET'])
@fresh_jwt_required
def get_my_bots():
    """
    Returns bots created by the user.
    :return: A bots list
    """
    current_user = get_jwt_identity()
    list_bots = views.MyBotsManagement().get_bots(email=current_user)

    return jsonify(list_bots), 200


@resources.route('/mybots', methods=['POST'])
@fresh_jwt_required
def create_bots():
    """
    To create a new user bot
    :return: The bot created
    """
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


@resources.route('/mybots/<id_bot>', methods=['GET'])
@fresh_jwt_required
def generate_token_bot(id_bot):
    """
    Generate a token for the bot
    :param id_bot: ID of bot
    :return: The token
    """
    token_bot = create_access_token(identity=id_bot, expires_delta=False)
    views.MyBotsManagement().add_token(id=id_bot, token=token_bot)

    return jsonify(token_bot), 200


@resources.route('/mybots/<id_bot>', methods=['PUT'])
@fresh_jwt_required
def renew_token_bot(id_bot):
    """
    Update the token bot
    :param id_bot: ID of bot
    :return: The new token
    """
    token_bot = create_access_token(identity=id_bot, expires_delta=False)
    views.MyBotsManagement().add_token(id=id_bot, token=token_bot)

    return jsonify(token_bot), 200


@resources.route('/mybots/<id_bot>', methods=['DELETE'])
@fresh_jwt_required
def delete_bot(id_bot):
    """
    Delete a bot by Id
    :param id_bot: ID of bot
    :return: Successful operation
    """
    if id_bot:
        views.MyBotsManagement().delete(id=id_bot)
        return jsonify(msg.SUCCESS), 200
    return jsonify(msg.NO_DATA), 404


@resources.route('/bots', methods=['GET'])
@fresh_jwt_required
def get_bots():
    """
    Return all type bots created to attack. They are diferents with the scan bots created within page mybots
    :return: The list of bots
    """
    list_bots = views.BotsManagement().get()
    return jsonify(list_bots), 200


# -------------------------
# CONNECT WITH BOTS (CEMENT)
# -------------------------

@resources.route('/bots/login', methods=['POST'])
@jwt_required
def login_bot():
    """
    Logs bot into the API
    :return: The bot token
    """
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
    """
    Return the bot by scan id
    :return: The bot
    """
    bot_id = get_jwt_identity()
    bot_scans = views.ScanManagement().scans_by_bot(bot=bot_id)

    return jsonify(bot_scans), 200


@resources.route('/bots/geo/<id_scan>', methods=['POST'])
@fresh_jwt_required
def save_geo(id_scan):
    """
    Save geo info of a bot
    :param id_scan: Scan id
    :return: The id of document into database
    """
    data = request.json
    if not data:
        return jsonify(msg.NO_DATA), 400
    db_id = views.ScansDataManagement().create(scan=id_scan, data=data)
    return jsonify(db_id), 200


@resources.route('/bots/data/<id_scan>', methods=['POST'])
@fresh_jwt_required
def save_data(id_scan):
    """
    Save all information about a scan
    :param id_scan: Scan id
    :return: Successful operation
    """
    data = request.json
    if not data:
        return jsonify(msg.NO_DATA), 400
    for scan in data:
        views.ScansDataManagement().create(scan=id_scan, data=scan)
    return jsonify(msg.SUCCESS), 200


@resources.route('/bots/<name>/<host>/<id_scan>', methods=['POST'])
@fresh_jwt_required
def save_bot(name, host, id_scan):
    """
    Save the information about a bot in a separate collection
    :param name: Name of bot type
    :param host: The bot target
    :param id_scan: Scan id
    :return: Successful operation
    """
    data = request.json
    if not data:
        return jsonify(msg.NO_DATA), 400
    collection = ""
    if name == 'nobita':
        for d in data:
            collection = generic_model.Generic().create_nobita(name=name, host=host, id=id_scan, data=d)
    else:
        collection = generic_model.Generic().create(name=name, host=host, id=id_scan, data=data)
    if collection:
        return jsonify(msg.SUCCESS), 200


@resources.route('/bots/update_done/<scan_id>', methods=['PUT'])
@fresh_jwt_required
def update_done(scan_id):
    """
    Update the done field in document
    :param scan_id: Scan id
    :return: Successful operation
    """
    views.ScanManagement().change_done(id=scan_id, value=True)
    views.ScanManagement().change_launch(id=scan_id, value=False)
    return jsonify(msg.SUCCESS), 200


@resources.route('/upload', methods=['POST'])
@fresh_jwt_required
def upload_file():
    """
    Upload a new type of bot
    :return: Successful operation
    """
    # First save name and description in database
    name = request.form.get('name')
    description = request.form.get('description')
    res = views.BotsManagement().create(name=name, description=description)
    if not res:
        return jsonify(msg.ERROR_SAVE_DATABASE)
    # Then, save the file to a local directory
    if 'file' not in request.files:
        return jsonify(msg.NO_DATA), 400
    file = request.files['file']
    # if user does not select file, browser also
    # submit an empty part without filename
    if file.filename == '':
        return jsonify(msg.NO_DATA), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return jsonify(msg.SUCCESS), 200


@resources.route('/download/<type_bot>', methods=['GET'])
@fresh_jwt_required
def download_file(type_bot):
    """
    Download bot files
    :param type_bot: Bot name
    :return: The bot file
    """
    bot = type_bot + '.py'
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               bot, as_attachment=True)
