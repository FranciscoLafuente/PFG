# coding=utf-8

from flask import request, jsonify
from flask_jwt_extended import (fresh_jwt_required, get_jwt_identity)
from . import resources
from app.respository import views
from app.respository import generic_model
from app.methods import send_to_queue
from app.static import messages as msg
from bson import ObjectId
import socket


@resources.route('/myproject', methods=['GET'])
@fresh_jwt_required
def get_projects():
    """
    Get all projects by user
    :return: A list of projects
    """
    list_projects = []
    current_user = get_jwt_identity()
    id_projects = views.UserManagement().projects_id(email=current_user)
    for p in id_projects:
        list_projects.append(views.ProjectManagement().project(id=p))

    return jsonify(list_projects), 200


@resources.route('/myproject', methods=['POST'])
@fresh_jwt_required
def add_project():
    """
    Adds an new project to user
    :return: The project created
    """
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


@resources.route('/myproject/<id>', methods=['GET'])
@fresh_jwt_required
def get_scans(id):
    """
    Returns scans of the project id
    :param id: Project id
    :return: A list of scans
    """
    list_scans = []
    s_id = views.ProjectManagement().scans_id(id=id)
    for scan in s_id:
        list_scans.append(views.ScanManagement().get_scan(id=scan))

    return jsonify(list_scans), 200


@resources.route('/myproject/<id>', methods=['POST'])
@fresh_jwt_required
def add_scan(id):
    """
    Adds a new scan in a project
    :param id: Project id
    :return: Success if everythin went well
    """
    if not request.is_json:
        return jsonify(msg.MISSING_JSON), 400

    scan_name = request.json.get('name', None)
    scan_bot = request.json.get('bot', None)
    scan_hosts = request.json.get('hosts', None)
    scan_executiontime = request.json.get('executiontime', None)

    if not scan_name or not scan_bot or not scan_hosts:
        return jsonify(msg.MISSING_PARAMETER), 400
    # Create scan
    id_bot = views.MyBotsManagement().get_id(name=scan_bot)
    scan_id = views.ScanManagement().create(name=scan_name, hosts=scan_hosts, bot=ObjectId(id_bot),
                                            execution_time=scan_executiontime)
    if not scan_id:
        return jsonify(msg.ALREADY_USE), 400
    views.ProjectManagement().add_scan(id=id, scan_id=scan_id)

    # Add scan to queue
    scan = views.ScanManagement().get_scan(id=scan_id)
    send_to_queue(scan)

    return jsonify(msg.SUCCESS), 200


@resources.route('/myproject/<id>', methods=['DELETE'])
@fresh_jwt_required
def delete_project(id):
    """
    Delete a project by id
    :param id: Project id
    :return: Success if everythin went well
    """
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


@resources.route('/myproject/scan/<scan_id>', methods=['POST'])
@fresh_jwt_required
def edit_bot(scan_id):
    """
    Change the assigned bot, in case it has been deleted
    :param scan_id: Scan id
    :return: Success if everythin went well
    """
    if not request.is_json:
        return jsonify(msg.MISSING_JSON), 400
    scan_bot = request.json.get('bot', None)
    # Get bot id and change it on scan
    bot_id = views.MyBotsManagement().get_id(name=scan_bot)
    views.ScanManagement().cahnge_bot(id=scan_id, bot=bot_id)
    return jsonify(msg.SUCCESS), 200


@resources.route('/myproject/scan/<scan_id>', methods=['PUT'])
@fresh_jwt_required
def relunch(scan_id):
    """
    Relunch the scan
    :param scan_id: Scan id
    :return: Success if everythin went well
    """
    views.ScanManagement().change_launch(id=scan_id, value=True)
    # Add scan to queue
    scan = views.ScanManagement().get_scan(id=scan_id)
    send_to_queue(scan)
    return jsonify(msg.SUCCESS), 200


@resources.route('/myproject/<id>/<id_scan>', methods=['DELETE'])
@fresh_jwt_required
def delete_scan(id, id_scan):
    """
    Delete a scan within a project
    :param id: Project id
    :param id_scan: Scan id
    :return: Success if everythin went well
    """
    scans_new = []
    id_obj = ObjectId(id_scan)
    scans_old = views.ProjectManagement().scans_id(id=id)
    for p in scans_old:
        if p != id_obj:
            scans_new.append(p)

    views.ScanManagement().delete(id=id_scan)
    views.ProjectManagement().update_scans(id=id, scans=scans_new)

    return jsonify(msg.SUCCESS), 200


@resources.route('/scan/<id>', methods=['GET'])
@fresh_jwt_required
def get_info(id):
    """
    Returns all the information getting in an attack on a single scan
    :param id: Scan id
    :return: A list with all information about scan
    """
    list_response = []
    hosts = views.ScanManagement().get_scan(id=id)['hosts']
    for h in hosts:
        scan = views.ScansDataManagement().one_scan(scan=id, domain=h)
        list_response.append(scan)
    if list_response:
        return jsonify(list_response), 200
    return jsonify(msg.NO_DATA), 404


@resources.route('/scan/<id>/<domain>', methods=['GET'])
@fresh_jwt_required
def get_timeline(id, domain):
    """
    Returns all information about a specific host within a scan, with all scans done over time(paginated).
    :param id: Scan id
    :param domain: A scan host
    :return: A list paginated with all scans
    """
    list_time = []
    page = request.args.get('page', 0, int)
    size = request.args.get('size', 0, int)
    scans = views.ScansDataManagement().get_scans_pag(scan=id, domain=domain, page=page, size=size)
    if not scans:
        return jsonify(msg.NO_DATA)
    for s in scans:
        list_time.append(s)
    return jsonify(list_time), 200


@resources.route('/scan/<id>/<domain>', methods=['POST'])
@fresh_jwt_required
def get_specific_scan(id, domain):
    """
    Returns a specific scan and can pass the number that specifies the chronological order as a parameter
    :param id: Scan id
    :param domain: A scan host
    :return: A specific scan
    """
    num = request.args.get('num', 0, int)
    scan = views.ScansDataManagement().get_scans(scan=id, domain=domain)
    if scan:
        return jsonify(scan[num]), 200
    return jsonify(msg.NO_DATA)


@resources.route('/scan/numItems/<id>/<domain>', methods=['GET'])
@fresh_jwt_required
def total_timeline(id, domain):
    """
    Return the number of scans done by domain
    :param id: Scan id
    :param domain: The domain scaned
    :return: Number of scans
    """
    scans = views.ScansDataManagement().scans_items(scan=id, domain=domain)
    if not scans:
        return jsonify(msg.NO_DATA), 404

    return jsonify(scans), 200


@resources.route('/bot/<name>/<id>', methods=['GET'])
@fresh_jwt_required
def bot_info(name, id):
    """
    Return the information about a specific type bot. For example Nobita, Suneo, etc. Only one of this.
    :param name: Bot type name
    :param id: Scan id
    :return: Info about bot
    """
    res = generic_model.Generic().read(name=name, id=id)
    return jsonify(res), 200


@resources.route('/search', methods=['GET'])
@fresh_jwt_required
def search_scan():
    """
    Search about a scan
    :return: The result of search
    """
    text = request.args.get('text', ":", str)
    res_list = text.split(':')
    page = request.args.get('page', 0, int)
    size = request.args.get('size', 0, int)
    if 'port' in res_list:
        r = generic_model.Generic().search(collection='nobita', port=res_list[1])
        response = [views.ScansDataManagement().get_by_id(id=r)]
    else:
        response = views.ScansDataManagement().search(key=res_list[0], searchText=res_list[1], start=page, end=size)

    return jsonify(response), 200


@resources.route('/search/numItems', methods=['GET'])
@fresh_jwt_required
def total_results():
    """
    Number of the results about a search done
    :return: The number of results
    """
    text = request.args.get('text', ":", str)
    res_list = text.split(':')
    response = views.ScansDataManagement().searchItems(key=res_list[0], searchText=res_list[1])

    return jsonify(response), 200
