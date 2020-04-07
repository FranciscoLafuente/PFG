# coding=utf-8

from flask import request, jsonify
from flask_jwt_extended import (fresh_jwt_required, get_jwt_identity)
from . import resources
from app.models import Scan, Project, AllBots
from app.respository import views
from bson import ObjectId


# MY PROJECT MANAGEMENT

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
    # TODO: queda por hacer, hay que crear en el repository los bots nobita, suneo, etc y devolver
    #  todos los datos obtenidos por cada bot
    s = Scan()
    domain = s.get_domain(id_scan)
    data = AllBots()
    response = data.get_data(domain)
    if not response:
        return jsonify({'msg': "Don't found data"})

    return jsonify(response), 200


@resources.route('/myproject', methods=['POST'])
@fresh_jwt_required
def add_project():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    project_name = request.json.get('name', None)
    project_type = request.json.get('type', None)

    if not project_name or not project_type:
        return jsonify({"msg": "Missing parameter"}), 400

    current_user = get_jwt_identity()
    project = views.ProjectManagement().create(name=project_name, type=project_type)
    views.UserManagement().add_project(user=current_user, id=ObjectId(project['id']))

    return jsonify(project), 200


@resources.route('/myproject/<id>', methods=['POST'])
@fresh_jwt_required
def add_scan(id):
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    scan_name = request.json.get('name', None)
    scan_bot = request.json.get('bot', None)
    scan_hosts = request.json.get('hosts', None)
    scan_executiontime = request.json.get('executiontime', None)

    if not scan_name or not scan_bot or not scan_hosts or not scan_executiontime:
        return jsonify({"msg": "Missing parameter"}), 400

    scan_id = views.ScanManagement().create(name=scan_name, hosts=scan_hosts, bot=ObjectId(scan_bot),
                                            execution_time=scan_executiontime)
    views.ProjectManagement().add_scan(id=id, scan_id=scan_id)

    return jsonify({"msg": "Success!"}), 200


@resources.route('/myproject/scan/<scan_id>', methods=['PUT'])
def relunch(scan_id):
    views.ScanManagement().change_done(id=scan_id, value=False)
    return jsonify({"msg": "Success!"}), 200


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

        views.ProjectManagement().delete(id=id)
        views.UserManagement().update_projects(email=current_user, projects=projects_new)
        return jsonify({"msg": "Success!"}), 200

    return jsonify({"msg": "Project not found"}), 404


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

    return jsonify({"msg": "Success!"}), 200
