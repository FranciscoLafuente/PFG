from werkzeug.security import generate_password_hash, check_password_hash
from flask import render_template
from . import mongo
import json
from bson import ObjectId
from datetime import datetime
import unicodedata
import requests
from .email import send_email


class User:

    def insert(self, collection):
        # Comprobar que el email no esta ya registrado
        user_collection = mongo.db.users
        user = user_collection.find_one({'email': collection['email']})

        # Insertar si el email no esta en uso
        if user is None:
            user_collection.insert({
                'email': collection['email'],
                'name': collection['name'],
                'password': self.password(collection['password']),
                'projects': [],
                'created': time_str()
            })

    def get_user(self, email):
        u = mongo.db.users.find_one({'email': email})
        user = {}
        p = Project()
        if u is not None:
            user = {
                'email': u['email'],
                'name': u['name'],
                'projects': p.get_projects(email)
            }

        return user

    def update_user_projects(self, projects, user):
        # Update user projects
        mongo.db.users.update(
            {'email': user},
            {'$set': {'projects': projects}})

    def check_user(self, collection):
        user_register = mongo.db.users.find_one({
            'email': collection['email']
        })

        if user_register is None:  # Si el email no existe
            return False
        else:  # Devuelve si la password es correcta o no
            return self.verify_password(user_register['password'], collection['password'])

    def password(self, password):
        return generate_password_hash(password)

    def verify_password(self, hash_password, password):
        return check_password_hash(hash_password, password)


class Project:

    def get_projects(self, user):
        current_user = mongo.db.users.find_one({'email': user})
        projects = current_user.get('projects')

        list_pro = []
        for p in projects:
            pro = mongo.db.projects.find_one({'_id': ObjectId(p)})
            list_pro.append(json.loads(JSONEncoder().encode(pro)))

        return list_pro

    def get_oneProject(self, id_project):
        return mongo.db.projects.find_one({'_id': ObjectId(id_project)})

    def create_projetc(self, user, name, is_public):
        p = unicodedata.normalize('NFKD', is_public).encode('ascii', 'ignore')
        product_type = False
        if "Public" in p:
            product_type = True

        # Insert in collection projects
        project = mongo.db.projects.insert({
            'name': name,
            'type': product_type,  # If is public: 1 True, 0 False
            'scans': [],
            'created': time_str()
        })

        # Update user projects
        mongo.db.users.update(
            {'email': user},
            {'$push': {'projects': project}})

        return json.loads(JSONEncoder().encode(mongo.db.projects.find_one({'_id': ObjectId(project)})))

    def project_with_scans(self, user):
        s = Scan()
        projects = self.get_projects(user)
        list = []
        for p in projects:
            p['scans'] = s.get_scans(str(p['_id']))
            list.append(p)

        return list

    def delete_project(self, project_id, user):
        # Delete a project in users
        p_str = JSONEncoder().encode(project_id)
        update_projects = []
        current_user = mongo.db.users.find_one({'email': user})
        projects = current_user.get('projects')
        for p in projects:
            p_change = JSONEncoder().encode(p)
            if p_change != p_str:
                update_projects.append(ObjectId(p))

        u = User()
        u.update_user_projects(update_projects, user)
        # Delete a project in projects
        p_delete = mongo.db.projects.delete_one({'_id': ObjectId(project_id)})

        return p_delete


class Scan:

    def create_scan(self, user, id_project, name_scan, bots, hosts, executiontime):
        b = Bot()
        listbots_id = []
        list_bots = b.get_bots(user)
        for bot in list_bots:
            b_name = bot['name']
            if b_name in bots:
                listbots_id.append(ObjectId(bot['_id']))

        new_scan = mongo.db.scans.insert({
            "name": name_scan,
            "bots": listbots_id,
            "executiontime": executiontime,
            "hosts": hosts,
            'created': time_str(),
            'done': False
        })

        # Update project with the new scan
        mongo.db.projects.update(
            {'_id': ObjectId(id_project)},
            {'$push': {"scans": new_scan}}
        )
        scan_created = mongo.db.scans.find_one({'_id': ObjectId(new_scan)})
        return json.loads(JSONEncoder().encode(scan_created))

    def get_scans(self, id_project):
        project = mongo.db.projects.find_one({'_id': ObjectId(id_project)})
        scans_project = project.get('scans')
        list_s = []
        for s in scans_project:
            scan = mongo.db.scans.find_one({'_id': ObjectId(s)})
            list_s.append(json.loads(JSONEncoder().encode(scan)))

        return list_s

    def get_scans_by_bot(self, id_bot):
        list_s = []
        for scan in mongo.db.scans.find({'bots': ObjectId(id_bot)}):
            list_s.append(json.loads(JSONEncoder().encode(scan)))

        return list_s

    def change_done(self, scan_id):
        update = mongo.db.scans.update(
            {'_id': ObjectId(scan_id)},
            {'$set': {"done": True}}
        )
        return update

    def update_scan_bots(self, scan, id_bot):
        list_update = []
        bot_str = JSONEncoder().encode(id_bot)
        # Get all bots in a specific scan
        bots = scan['bots']
        for b in bots:
            b_str = JSONEncoder().encode(b)
            if b_str != bot_str:
                list_update.append(b)

        update = mongo.db.scans.update(
            {'_id': ObjectId(scan['_id'])},
            {'$set': {"bots": list_update}}
        )
        return update


class Bot:

    def create_bot(self, name, user, ip, type_bot):
        mongo.db.bots.insert({
            "name": name,
            "email": user,
            "ip": ip,
            "type": type_bot,
            "token": "",
            'created': time_str()
        })

        b = mongo.db.bots.find_one({"name": name, 'email': user})

        return json.loads(JSONEncoder().encode(b))

    def get_bots(self, user):
        list_bots = []
        for bot in mongo.db.bots.find({'email': user}):
            list_bots.append(json.loads(JSONEncoder().encode(bot)))

        return list_bots

    def search_bot(self, ip_bot, id_bot):
        b = mongo.db.bots.find_one({"_id": ObjectId(id_bot), "ip": ip_bot})
        if b:
            return b['type']
        return None

    def add_token(self, id_bot, token):
        b = mongo.db.bots.find_one({"_id": ObjectId(id_bot)})
        # Update bot with the generated token
        bot_update = mongo.db.bots.update(
            {'_id': b['_id']},
            {'$set': {"token": token}}
        )

        return json.loads(JSONEncoder().encode(mongo.db.bots.find_one({"_id": ObjectId(id_bot)})))

    def delete_bot(self, id_bot):
        change = False
        s = Scan()
        scans = s.get_scans_by_bot(id_bot)
        for sc in scans:
            update = s.update_scan_bots(sc, id_bot)
            if update['updatedExisting']:
                change = True
                mongo.db.bots.delete_one({'_id': ObjectId(id_bot)})
        return change


class Nobita:

    def save_scan(self, scan):
        geo = self.geo_ip(scan['ip_address'])
        complete = mongo.db.nobita_bot.insert_one({'ip_address': scan['ip_address'], 'country': geo['country'],
                                                   'city': geo['city'], 'region_name': geo['regionName'],
                                                   'isp': geo['isp'], 'port': scan['port'], 'banner': scan['banner'],
                                                   'latitud': geo['lat'], 'longitud': geo['lon'], 'zip': geo['zip']})
        return complete

    def geo_ip(self, ip):
        url = "http://ip-api.com/json/" + ip
        response = requests.get(url)
        json_obj = response.json()
        return json_obj


class Shizuka:

    def save_ipreverse(self, data):
        d_insert = mongo.db.shizuka_bot.find_one({'domain': data['domain']})
        if d_insert is None:
            return mongo.db.shizuka_bot.insert_many(data)
        return d_insert


class Suneo:

    def save_domain(self, data):
        d_insert = mongo.db.suneo_bot.find_one({'domain': data['domain']})
        if d_insert is None:
            return mongo.db.suneo_bot.insert_one(data)
        return d_insert


class Gigante:

    def save_ssh(self, data):
        d_insert = mongo.db.gigante_bot.find_one({'domain': data['domain']})
        if d_insert is None:
            return mongo.db.gigante_bot.insert_one(data)
        return d_insert


def time_str():
    now = datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)
