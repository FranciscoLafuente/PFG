# coding=utf-8

from flask import request, jsonify
from flask_jwt_extended import (JWTManager, jwt_required, create_access_token, get_jwt_identity)
from . import main
from ..models import User, Project, Scan


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
    access_token = create_access_token(identity=useremail)
    return jsonify(access_token=access_token), 200


@main.route('/myprofile', methods=['GET'])
@jwt_required
def get_user():
    current_user = get_jwt_identity()
    u = User()
    print(current_user)

    return jsonify(u.get_user(current_user)), 200


@main.route('/myproject', methods=['GET'])
@jwt_required
def get_products():
    current_user = get_jwt_identity()
    project_user = Project()
    all_projects = project_user.project_with_scans(current_user)
    print(all_projects)

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

    if not scan_name or not scan_bots or not scan_hosts:
        return jsonify({"msg": "Missing parameter"}), 400

    s = Scan()
    s.create_scan(id, scan_name, scan_bots, scan_hosts)

    # Return all projects update
    current_user = get_jwt_identity()
    project_user = Project()
    all_projects = project_user.project_with_scans(current_user)

    return jsonify(all_projects), 200


@main.route('/bots', methods=['GET'])
@jwt_required
def bots():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200
