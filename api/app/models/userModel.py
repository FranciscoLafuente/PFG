from werkzeug.security import generate_password_hash, check_password_hash
from .. import mongo
from ..models import time_str, JSONEncoder
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

    def change_password(self, email, new_pass):
        u = mongo.db.users.find_one({'email': email})
        if u is not None:
            hash_password = self.password(new_pass)
            update = mongo.db.users.update(
                {'email': email},
                {'$set': {'password': hash_password}})
        return update

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