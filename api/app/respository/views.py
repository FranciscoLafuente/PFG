from werkzeug.security import generate_password_hash, check_password_hash
from .models import User, Project, Scan, Bot, HostIp, Nobita, Shizuka, Suneo, Gigante, GeoLocation
import json
from bson import ObjectId
import datetime
import requests
from mongoengine import errors
from pprint import pprint


class UserManagement:

    def create(self, data):
        password = self.password(data['password'])
        u = User(email=data['email'], name=data['name'], password=password)
        try:
            u.save()
            return True
        except errors.NotUniqueError:
            return False

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
        try:
            p.save()
            return json.loads(JSONEncoder().encode(
                dict({'id': p.id, 'name': p.name, 'type': p.type})
            ))
        except errors.NotUniqueError:
            return False

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
        if kwargs['execution_time']:
            s = Scan(name=kwargs['name'], hosts=kwargs['hosts'], bot=kwargs['bot'],
                     executionTime=kwargs['execution_time'])
        else:
            s = Scan(name=kwargs['name'], hosts=kwargs['hosts'], bot=kwargs['bot'])
        try:
            s.save()
            return s.id
        except errors.NotUniqueError:
            return False

    def get_scan(self, **kwargs):
        for s in Scan.objects(id=kwargs['id']):
            return json.loads(JSONEncoder().encode(
                dict({'id': s.id, 'name': s.name, 'hosts': s.hosts, 'created': s.created.strftime("%Y-%m-%d %H:%M:%S")})
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
                    dict({'id': s.id, 'hosts': s.hosts, 'executionTime': s.executionTime.strftime("%Y-%m-%d %H:%M:%S"),
                          'done': s.done})
                )))
        return scans_list


class BotManagement:

    def create(self, **kwargs):
        b = Bot(name=kwargs['name'], email=kwargs['email'], ip=kwargs['ip'], type=kwargs['type'])
        try:
            b.save()
            return json.loads(JSONEncoder().encode(
                dict({'id': b.id, 'ip': b.ip, 'name': b.name, 'type': b.type})
            ))
        except errors.NotUniqueError:
            return False

    def get_id(self, **kwargs):
        for b in Bot.objects(name=kwargs['name']):
            return b.id

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


class HostIpManagement:

    def create(self, **kwargs):
        h = HostIp(domain=kwargs['domain'], ip=kwargs['ip'])
        try:
            h.save()
            return True
        except errors.NotUniqueError:
            return False

    def get_host(self, **kwargs):
        for h in HostIp.objects(domain=kwargs['domain']):
            return dict({'id': h.id, 'domain': h.domain, 'ip': h.ip, 'created': h.created})

    def get_domain(self, **kwargs):
        for h in HostIp.objects(id=kwargs['id']):
            return h.domain


class NobitaManagement:

    def create(self, **kwargs):
        n = Nobita(
            ip=kwargs['data']['ip'],
            domain=kwargs['data']['domain'],
            port=kwargs['data']['port'],
            banner=kwargs['data']['banner'],
        )
        n.save()
        return n

    def get_nobita(self, **kwargs):
        nobita_list = []
        for n in Nobita.objects(domain=kwargs['domain']):
            nobita_list.append(
                json.loads(JSONEncoder().encode(
                    dict({'ip': n.ip, 'domain': n.domain, 'port': n.port, 'banner': n.banner})
                ))
            )
        return nobita_list


class ShizukaManagement:

    def create(self, **kwargs):
        shi = Shizuka(ip=kwargs['data']['ip'], target=kwargs['data']['target'], domain=kwargs['data']['domain'])
        try:
            shi.save()
        except errors.NotUniqueError:
            pass

    def get_shizuka(self, **kwargs):
        shizuka_list = []
        for shi in Shizuka.objects(target=kwargs['domain']):
            shizuka_list.append(
                json.loads(JSONEncoder().encode(
                    dict({'ip': shi.ip, 'target': shi.target, 'domain': shi.domain})
                ))
            )
        return shizuka_list


class SuneoManagement:

    def create(self, **kwargs):
        su = Suneo(ip=kwargs['data']['ip'], domain=kwargs['data']['domain'], cms=kwargs['data']['cms'],
                   technologies=kwargs['data']['technologies'])
        try:
            su.save()
        except errors.NotUniqueError:
            pass

    def get_suneo(self, **kwargs):
        for su in Suneo.objects(domain=kwargs['domain']):
            return json.loads(JSONEncoder().encode(
                dict({'cms': su.cms, 'technologies': su.technologies})
            ))


class GiganteManagement:

    def create(self, **kwargs):
        pass

    def get_shizuka(self, **kwargs):
        for gi in Gigante.objects(domain=kwargs['domain']):
            return gi.to_json()


class GeoLocationManagement:

    def create(self, **kwargs):
        g = geo_ip(kwargs['domain'])
        geo = GeoLocation(
            ip=kwargs['ip'],
            domain=kwargs['domain'],
            country=g['country'],
            org=g['org'],
            city=g['city'],
            region_name=g['regionName'],
            isp=g['isp'],
            lat=g['lat'],
            lon=g['lon'],
            zip=g['zip'],
        )
        try:
            geo.save()
        except errors.NotUniqueError:
            pass

    def get_geo(self, **kwargs):
        for g in GeoLocation.objects(domain=kwargs['domain']):
            return json.loads(JSONEncoder().encode(
                dict({
                    'ip': g.ip, 'domain': g.domain, 'country': g.country, 'org': g.org, 'city': g.city,
                    'region_name': g.region_name, 'isp': g.isp, 'lat': g.lat, 'lon': g.lon, 'zip': g.zip
                })
            ))


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
