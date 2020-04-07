from werkzeug.security import generate_password_hash, check_password_hash
from .models import User, Project, Scan, Bot, Nobita, Shizuka, Suneo, Gigante
import json
from bson import ObjectId
import datetime
import requests


class UserManagement:

    def create(self, data):
        password = self.password(data['password'])
        u = User(email=data['email'], name=data['name'], password=password)
        u.save()

    def change_password(self, **kwargs):
        password = self.password(kwargs['password'])
        for user in User.objects(email=kwargs['email']):
            u = User.objects(user.email).update_one(set__password=password)
            u.reload()
            return True
        return False

    def exists(self, **kwargs):
        for user in User.objects(email=kwargs['email']):
            return user.email

    def check(self, **kwargs):
        for user in User.objects(email=kwargs['email']):
            return check_password_hash(user.password, kwargs['password'])
        return False

    def add_project(self, **kwargs):
        for user in User.objects(email=kwargs['user']):
            User.objects(id=user.id).update(push__projects=kwargs['id'])
            return True

    def update_projects(self, **kwargs):
        for user in User.objects(email=kwargs['email']):
            User.objects(id=user.id).update(set__projects=kwargs['projects'])
            return True

    def projects_id(self, **kwargs):
        for user in User.objects(email=kwargs['email']):
            return user.projects

    def password(self, password):
        return generate_password_hash(password)


class ProjectManagement:

    def create(self, **kwargs):
        p = Project(name=kwargs['name'], type=kwargs['type'])
        p.save()
        return json.loads(JSONEncoder().encode(
            dict({'id': p.id, 'name': p.name, 'type': p.type})
        ))

    def project(self, **kwargs):
        for p in Project.objects(id=kwargs['id']):
            return json.loads(JSONEncoder().encode(
                dict({'id': p.id, 'name': p.name, 'type': p.type})
            ))

    def add_scan(self, **kwargs):
        for p in Project.objects(id=kwargs['id']):
            Project.objects(id=p.id).update(push__scans=kwargs['scan_id'])
            return True

    def scans_id(self, **kwargs):
        for p in Project.objects(id=kwargs['id']):
            return p.scans

    def delete(self, **kwargs):
        Project.objects(id=kwargs['id']).delete()

    def update_scans(self, **kwargs):
        for p in Project.objects(id=kwargs['id']):
            Project.objects(id=p.id).update(set__scans=kwargs['scans'])
            return True


class ScanManagement:

    def create(self, **kwargs):
        s = Scan(name=kwargs['name'], hosts=kwargs['hosts'], bot=kwargs['bot'],
                 executionTime=kwargs['execution_time'])
        s.save()
        return s.id

    def get_scan(self, **kwargs):
        for s in Scan.objects(id=kwargs['id']):
            return json.loads(JSONEncoder().encode(
                dict({'id': s.id, 'hosts': s.hosts, 'created': s.created.strftime("%Y-%m-%d %H:%M:%S")})
            ))

    def change_done(self, **kwargs):
        for s in Scan.objects(id=kwargs['id']):
            Scan.objects(id=s.id).update(set__done=kwargs['value'])

    def delete(self, **kwargs):
        Scan.objects(id=kwargs['id']).delete()

    def scans_by_bot(self, **kwargs):
        scans_list = []
        for s in Scan.objects(bot=ObjectId(kwargs['bot'])):
            scans_list.append(
                json.loads(JSONEncoder().encode(
                    dict({'hosts': s.hosts, 'done': s.done})
                )))
        return scans_list


class BotManagement:

    def create(self, **kwargs):
        b = Bot(name=kwargs['name'], email=kwargs['email'], ip=kwargs['ip'], type=kwargs['type'])
        b.save()
        return json.loads(JSONEncoder().encode(
            dict({'id': b.id, 'ip': b.ip, 'name': b.name, 'type': b.type})
        ))

    def get_bots(self, **kwargs):
        list_bots = []
        for b in Bot.objects(email=kwargs['email']):
            list_bots.append(
                json.loads(JSONEncoder().encode(
                    dict({'id': b.id, 'ip': b.ip, 'name': b.name, 'type': b.type, 'token': b.token})
                )))
        return list_bots

    def add_token(self, **kwargs):
        for b in Bot.objects(id=kwargs['id']):
            Bot.objects(id=b.id).update(set__token=kwargs['token'])

    def delete(self, **kwargs):
        Bot.objects(id=kwargs['id']).delete()

    def search_bot(self, **kwargs):
        for b in Bot.objects(id=kwargs['id'], ip=kwargs['ip']):
            return b.type


class NobitaManagement:

    def create(self, **kwargs):
        geo = geo_ip(kwargs['data']['ip_address'])
        n = Nobita(
            ip=kwargs['data']['ip_address'],
            domain=kwargs['data']['domain'],
            port=kwargs['data']['port'],
            banner=kwargs['data']['banner'],
            country=geo['country'],
            city=geo['city'],
            region_name=geo['regionName'],
            isp=geo['isp'],
            latitud=geo['lat'],
            longitud=geo['lon'],
            zip=geo['zip'],
        )
        n.save()
        return n


class ShizukaManagement:

    def create(self, **kwargs):
        shi = Shizuka(ip=kwargs['data']['ip_address'], target=kwargs['data']['target'], domain=kwargs['data']['domain'])
        shi.save()
        return shi


class SuneoManagement:

    def create(self, **kwargs):
        su = Suneo(ip=kwargs['data']['ip_address'], domain=kwargs['data']['domain'], cms=kwargs['data']['cms'])
        su.save()
        return su


class GiganteManagement:

    def create(self, **kwargs):
        pass


def geo_ip(ip):
    url = "http://ip-api.com/json/" + ip
    response = requests.get(url)
    json_obj = response.json()
    return json_obj


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)
