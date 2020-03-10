from werkzeug.security import generate_password_hash, check_password_hash
from . import mongo
import json
from bson import ObjectId


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
                'projects': []
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
        product_type = False
        if is_public is 1:
            product_type = True

        # Insert in collection projects
        project = mongo.db.projects.insert({
            'name': name,
            'type': product_type,  # If is public: 1 True, 0 False
            'scans': []
        })

        # Update user projects
        mongo.db.users.update(
            {'email': user},
            {'$push': {'projects': project}})

    def project_with_scans(self, user):
        s = Scan()
        projects = self.get_projects(user)
        list = []
        for p in projects:
            p['scans'] = s.get_scans(str(p['_id']))
            list.append(p)

        return list


class Scan:

    def create_scan(self, user, id_project, name_scan, bots, hosts):
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
            "executiontime": "01/01/1612",
            "hosts": hosts
        })

        # Update project with the new scan
        mongo.db.projects.update(
            {'_id': ObjectId(id_project)},
            {'$push': {"scans": new_scan}}
        )

        p = Project()
        project_update = p.get_oneProject(id_project)

        return json.loads(JSONEncoder().encode(project_update))

    def get_scans(self, id_project):
        project = mongo.db.projects.find_one({'_id': ObjectId(id_project)})
        scans_project = project.get('scans')
        list_s = []
        for s in scans_project:
            scan = mongo.db.scans.find_one({'_id': ObjectId(s)})
            list_s.append(json.loads(JSONEncoder().encode(scan)))

        return list_s


class Bot:

    def create_bot(self, name, user, ip, type_bot):
        mongo.db.bots.insert({
            "name": name,
            "email": user,
            "ip": ip,
            "type": type_bot,
        })

        b = mongo.db.bots.find_one({"name": name, 'email': user})

        return json.loads(JSONEncoder().encode(b))

    def get_bots(self, user):
        list_bots = []
        for bot in mongo.db.bots.find({'email': user}):
            list_bots.append(json.loads(JSONEncoder().encode(bot)))

        return list_bots


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)
