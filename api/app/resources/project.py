# coding=utf-8

from flask import request, jsonify
from flask_jwt_extended import (fresh_jwt_required, get_jwt_identity)
from . import resources
from app.models import Scan, Project, AllBots


# MY PROJECT MANAGEMENT

@resources.route('/myproject', methods=['GET'])
@fresh_jwt_required
def get_products():
    current_user = get_jwt_identity()
    project_user = Project()
    all_projects = project_user.project_with_scans(current_user)

    return jsonify(all_projects), 200


@resources.route('/myproject/<id_p>', methods=['GET'])
@fresh_jwt_required
def get_scans(id_p):
    s = Scan()
    all_scans = s.get_scans(id_p)

    return jsonify(all_scans), 200


@resources.route('/scan/<id_scan>', methods=['GET'])
@fresh_jwt_required
def get_info(id_scan):
    s = Scan()
    domain = s.get_domain(id_scan)
    data = AllBots()
    response = data.get_data(domain)
    print(response)

    return jsonify(response), 200


@resources.route('/myproject', methods=['POST'])
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


@resources.route('/myproject/<id>', methods=['POST'])
@fresh_jwt_required
def add_scan(id):
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


@resources.route('/myproject/scan/<scan_id>', methods=['PUT'])
def relunch(scan_id):
    s = Scan()
    update = s.change_done(scan_id, False)
    if update is None:
        return jsonify({"msg": "Scan not found"}), 404
    return jsonify({"msg": "Success!"}), 200


@resources.route('/myproject/<id>', methods=['DELETE'])
@fresh_jwt_required
def delete_project(id):
    current_user = get_jwt_identity()
    if id is not None:
        p = Project()
        is_delete = p.delete_project(id, current_user)
        if is_delete:
            return jsonify({"msg": "Success!"}), 200
    return jsonify({"msg": "Project not found"}), 404


@resources.route('/myproject/<id_p>/<id_scan>', methods=['DELETE'])
@fresh_jwt_required
def delete_scan(id_p, id_scan):
    if id_scan:
        s = Scan()
        is_delete = s.delete_scan(id_p, id_scan)
        if is_delete:
            return jsonify({"msg": "Success!"}), 200
    return jsonify({"msg": "Project not found"}), 404
