# coding=utf-8

from flask import request, jsonify
from flask_jwt_extended import (fresh_jwt_required, get_jwt_identity)
from . import resources
from app.respository import views
from app.respository import generic_model
from bson import ObjectId
import socket
import builtwith
from app.static import messages as msg


@resources.route('/myproject', methods=['GET'])
@fresh_jwt_required
def get_projects():
    list_projects = []
    current_user = get_jwt_identity()
    id_projects = views.UserManagement().projects_id(email=current_user)
    for p in id_projects:
        list_projects.append(views.ProjectManagement().project(id=p))

    return jsonify(list_projects), 200


@resources.route('/myproject/<id_p>', methods=['GET'])
@fresh_jwt_required
def get_scans(id_p):
    list_scans = []
    s_id = views.ProjectManagement().scans_id(id=id_p)
    for scan in s_id:
        list_scans.append(views.ScanManagement().get_scan(id=scan))

    return jsonify(list_scans), 200


@resources.route('/scan/<id_scan>', methods=['GET'])
@fresh_jwt_required
def get_info(id_scan):
    list_response = []
    hosts = views.ScanManagement().get_scan(id=id_scan)['hosts']
    for h in hosts:
        scan = views.ScansDataManagement().one_scan(scan=id_scan, domain=h)
        list_response.append(scan)
    if list_response:
        return jsonify(list_response), 200
    return jsonify(msg.NO_DATA)


@resources.route('/bot/<name>/<id>', methods=['GET'])
@fresh_jwt_required
def bot_info(name, id):
    res = generic_model.Generic().read(name=name, id=id)
    return jsonify(res), 200


@resources.route('/scan/<id_scan>/<domain>', methods=['GET'])
@fresh_jwt_required
def get_timeline(id_scan, domain):
    list_time = []
    scans = views.ScansDataManagement().get_scans(scan=id_scan, domain=domain)
    if not scans:
        return jsonify(msg.NO_DATA)
    for s in scans:
        list_time.append(s)
    return jsonify(list_time), 200


@resources.route('/scan/<id_scan>/<domain>/<num>', methods=['GET'])
@fresh_jwt_required
def get_specific_scan(id_scan, domain, num):
    scan = views.ScansDataManagement().one_scan(scan=id_scan, domain=domain)
    if scan:
        return jsonify(scan), 200
    return jsonify(msg.NO_DATA)


@resources.route('/myproject', methods=['POST'])
@fresh_jwt_required
def add_project():
    if not request.is_json:
        return jsonify(msg.MISSING_JSON), 400

    project_name = request.json.get('name', None)
    project_type = request.json.get('type', None)

    if not project_name or not project_type:
        return jsonify(msg.MISSING_PARAMETER), 400
    # Convert project_type to Boolean
    if project_type == 'True':
        project_type = True
    else:
        project_type = False

    current_user = get_jwt_identity()
    project = views.ProjectManagement().create(name=project_name, type=project_type)
    if not project:
        return jsonify(msg.ALREADY_USE), 400
    views.UserManagement().add_project(user=current_user, id=ObjectId(project['id']))

    return jsonify(project), 200


@resources.route('/myproject/<id>', methods=['POST'])
@fresh_jwt_required
def add_scan(id):
    if not request.is_json:
        return jsonify(msg.MISSING_JSON), 400

    scan_name = request.json.get('name', None)
    scan_bot = request.json.get('bot', None)
    scan_hosts = request.json.get('hosts', None)
    scan_executiontime = request.json.get('executiontime', None)

    if not scan_name or not scan_bot or not scan_hosts:
        return jsonify(msg.MISSING_PARAMETER), 400
    # Create scan
    id_bot = views.BotManagement().get_id(name=scan_bot)
    scan_id = views.ScanManagement().create(name=scan_name, hosts=scan_hosts, bot=ObjectId(id_bot),
                                            execution_time=scan_executiontime)
    if not scan_id:
        return jsonify(msg.ALREADY_USE), 400
    views.ProjectManagement().add_scan(id=id, scan_id=scan_id)

    return jsonify(msg.SUCCESS), 200


@resources.route('/myproject/scan/<scan_id>', methods=['POST'])
@fresh_jwt_required
def edit_bot(scan_id):
    if not request.is_json:
        return jsonify(msg.MISSING_JSON), 400
    scan_bot = request.json.get('bot', None)
    # Get bot id and change it on scan
    bot_id = views.BotManagement().get_id(name=scan_bot)
    views.ScanManagement().cahnge_bot(id=scan_id, bot=bot_id)
    return jsonify(msg.SUCCESS), 200


@resources.route('/myproject/scan/<scan_id>', methods=['PUT'])
@fresh_jwt_required
def relunch(scan_id):
    views.ScanManagement().change_done(id=scan_id, value=False)
    return jsonify(msg.SUCCESS), 200


@resources.route('/myproject/<id>', methods=['DELETE'])
@fresh_jwt_required
def delete_project(id):
    if id:
        projects_new = []
        id_obj = ObjectId(id)
        current_user = get_jwt_identity()
        projects_old = views.UserManagement().projects_id(email=current_user)
        for p in projects_old:
            if p != id_obj:
                projects_new.append(p)

        # Delete the scans that the project owns
        scans = views.ProjectManagement().scans_id(id=id)
        for scan in scans:
            views.ScanManagement().delete(id=ObjectId(scan))
        # Delete project
        views.ProjectManagement().delete(id=id)
        # Delete user project
        views.UserManagement().update_projects(email=current_user, projects=projects_new)
        return jsonify(msg.SUCCESS), 200

    return jsonify(msg.NO_DATA), 404


@resources.route('/myproject/<id_p>/<id_scan>', methods=['DELETE'])
@fresh_jwt_required
def delete_scan(id_p, id_scan):
    scans_new = []
    id_obj = ObjectId(id_scan)
    scans_old = views.ProjectManagement().scans_id(id=id_p)
    for p in scans_old:
        if p != id_obj:
            scans_new.append(p)

    views.ScanManagement().delete(id=id_scan)
    views.ProjectManagement().update_scans(id=id_p, scans=scans_new)

    return jsonify(msg.SUCCESS), 200


def get_all_data(domain):
    list_data = []
    # Create geoLocation
    '''
    ip = socket.gethostbyname(domain)
    views.GeoLocationManagement().create(ip=ip, domain=domain)
    '''
    # Save all scans in a list
    n = views.NobitaManagement().get_nobita(domain=domain)
    n_dict = dict({"type": "nobita", "data": n})
    shi = views.ShizukaManagement().get_shizuka(domain=domain)
    shi_dict = dict({"type": "shizuka", "data": shi})
    su = views.SuneoManagement().get_suneo(domain=domain)
    su_dict = dict({"type": "suneo", "data": su})
    geo = views.GeoLocationManagement().get_geo(domain=domain)
    geo_dict = dict({"type": "geo", "data": geo})
    list_data.append(n_dict)
    list_data.append(shi_dict)
    list_data.append(su_dict)
    list_data.append(geo_dict)
    return list_data
