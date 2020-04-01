# coding=utf-8

from flask import request, jsonify
from flask_jwt_extended import (JWTManager, jwt_required, fresh_jwt_required, create_access_token, get_jwt_identity,
                                decode_token)
from . import resources
from ..models import *
import datetime
import jwt


# MY PROJECT MANAGEMENT

@resources.route('/myproject', methods=['GET'])
@fresh_jwt_required
def get_products():
    current_user = get_jwt_identity()
    project_user = Project()
    all_projects = project_user.project_with_scans(current_user)

    return jsonify(all_projects), 200


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
