from .. import mongo
from ..models import time_str, JSONEncoder
import json
from bson import ObjectId


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
        p = JSONEncoder().encode(is_public)
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
