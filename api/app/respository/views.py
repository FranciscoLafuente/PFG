from werkzeug.security import generate_password_hash, check_password_hash
from .models import User, Project, Scan, ScansData, MyBots, Bots, Nobita, Shizuka, Suneo, Gigante, GeoLocation
import json
from bson import ObjectId
import datetime
from mongoengine import errors
from mongoengine.queryset.visitor import Q


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
                dict({'id': p.id, 'name': p.name, 'type': p.type, 'scans': p.scans})
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
                dict({'id': s.id, 'name': s.name, 'hosts': s.hosts, 'created': s.created.strftime("%Y-%m-%d %H:%M:%S"),
                      'done': s.done})
            ))

    def change_done(self, **kwargs):
        for s in Scan.objects(id=kwargs['id']):
            Scan.objects(id=s.id).update(set__done=kwargs['value'])

    def cahnge_bot(self, **kwargs):
        for s in Scan.objects(id=kwargs['id']):
            Scan.objects(id=s.id).update(set__bot=kwargs['bot'])

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


class ScansDataManagement:

    def create(self, **kwargs):
        try:
            s = ScansData(scan_user=kwargs['scan'])
            s.domain = kwargs['data']['domain']
            s.ip = kwargs['data']['ip']
            s.country = kwargs['data']['country']
            s.continent = kwargs['data']['continent']
            s.latitude = kwargs['data']['latitude']
            s.longitude = kwargs['data']['longitude']
            s.organization = kwargs['data']['organization']
            s.results = kwargs['data']['results']
            s.save()
            return json.loads(JSONEncoder().encode({'id': s.id}))
        except Exception as e:
            print("[ScansData - Create]")
            print("Exception", e)

    def get_by_id(self, **kwargs):
        try:
            for s in ScansData.objects(id=kwargs['id']):
                return json.loads(JSONEncoder().encode(
                    dict({'id': s.id, 'scan_user': s.scan_user, 'domain': s.domain, 'results': s.results,
                          'created': s.created.strftime("%Y-%m-%d %H:%M:%S"), 'ip': s.ip, 'country': s.country,
                          'continent': s.continent, 'latitude': s.latitude, 'longitude': s.longitude,
                          'organization': s.organization})
                ))
        except Exception as e:
            print("[ScansData - Get By Id]")
            print("Exception", e)

    def store_results(self, **kwargs):
        try:
            for s in ScansData.objects(id=kwargs['id']):
                ScansData.objects(id=s.id).update(push__results=kwargs['list'])
        except Exception as e:
            print("[ScansData - Store Results]")
            print("Exception", e)

    def get_scans(self, **kwargs):
        list_scans = []
        try:
            for s in ScansData.objects(scan_user=kwargs['scan'], domain=kwargs['domain']):
                list_scans.append(
                    json.loads(JSONEncoder().encode(
                        dict({'id': s.id, 'scan_user': s.scan_user, 'domain': s.domain, 'results': s.results,
                              'created': s.created.strftime("%Y-%m-%d %H:%M:%S"), 'ip': s.ip, 'country': s.country,
                              'continent': s.continent, 'latitude': s.latitude, 'longitude': s.longitude,
                              'organization': s.organization})
                    ))
                )
            return list_scans
        except Exception as e:
            print(['ScansData - Get Scans'])
            print('Exception', e)

    def one_scan(self, **kwargs):
        try:
            for s in ScansData.objects(scan_user=kwargs['scan'], domain=kwargs['domain']):
                return json.loads(JSONEncoder().encode(
                    dict({'id': s.id, 'scan_user': s.scan_user, 'domain': s.domain, 'results': s.results,
                          'created': s.created.strftime("%Y-%m-%d %H:%M:%S"), 'ip': s.ip, 'country': s.country,
                          'continent': s.continent, 'latitude': s.latitude, 'longitude': s.longitude,
                          'organization': s.organization})
                ))
        except Exception as e:
            print(['ScansData'])
            print('Exception', e)

    def search(self, **kwargs):
        list_scans = []
        try:
            for s in ScansData.objects(
                    Q(continent=kwargs['searchText']) | Q(country=kwargs['searchText'])
                    | Q(organization=kwargs['searchText']) | Q(domain=kwargs['searchText'])
            ):
                list_scans.append(
                    json.loads(JSONEncoder().encode(
                        dict({'id': s.id, 'scan_user': s.scan_user, 'domain': s.domain, 'results': s.results,
                              'created': s.created.strftime("%Y-%m-%d %H:%M:%S"), 'ip': s.ip, 'country': s.country,
                              'continent': s.continent, 'latitude': s.latitude, 'longitude': s.longitude,
                              'organization': s.organization})
                    ))
                )
            return list_scans
        except Exception as e:
            print(['ScansData'])
            print('Exception', e)


class MyBotsManagement:

    def create(self, **kwargs):
        b = MyBots(name=kwargs['name'], email=kwargs['email'], ip=kwargs['ip'], type=kwargs['type'])
        try:
            b.save()
            return json.loads(JSONEncoder().encode(
                dict({'id': b.id, 'ip': b.ip, 'name': b.name, 'type': b.type})
            ))
        except errors.NotUniqueError:
            return False

    def get_id(self, **kwargs):
        for b in MyBots.objects(name=kwargs['name']):
            return b.id

    def get_bots(self, **kwargs):
        list_bots = []
        for b in MyBots.objects(email=kwargs['email']):
            list_bots.append(
                json.loads(JSONEncoder().encode(
                    dict({'id': b.id, 'ip': b.ip, 'name': b.name, 'type': b.type, 'token': b.token})
                )))
        return list_bots

    def get_all_bots(self):
        list_bots = []
        for b in MyBots.objects:
            list_bots.append(
                json.loads(JSONEncoder().encode(
                    dict({'id': b.id, 'ip': b.ip, 'name': b.name, 'type': b.type, 'token': b.token})
                )))
        return list_bots

    def add_token(self, **kwargs):
        for b in MyBots.objects(id=kwargs['id']):
            MyBots.objects(id=b.id).update(set__token=kwargs['token'])

    def delete(self, **kwargs):
        MyBots.objects(id=kwargs['id']).delete()

    def search_bot(self, **kwargs):
        for b in MyBots.objects(id=kwargs['id'], ip=kwargs['ip']):
            return b.type


class BotsManagement:

    def create(self, **kwargs):
        try:
            b = Bots(
                name=kwargs['name'],
                description=kwargs['description']
            )
            b.save()
            return b.id
        except Exception as e:
            print("[Bots in Create]")
            print("Exception", e)

    def get(self):
        try:
            list_bots = []
            for b in Bots.objects:
                list_bots.append(b.name)
            return list_bots
        except Exception as e:
            print("[Bots in Create]")
            print("Exception", e)


class NobitaManagement:

    def create(self, **kwargs):
        n = Nobita(
            ip=kwargs['data']['ip'],
            domain=kwargs['data']['domain'],
            port=kwargs['data']['port'],
            banner=kwargs['data']['banner'],
        )
        n.save()
        return n.id

    def get_nobita(self, **kwargs):
        nobita_list = []
        for n in Nobita.objects(domain=kwargs['domain']):
            nobita_list.append(
                json.loads(JSONEncoder().encode(
                    dict({'ip': n.ip, 'domain': n.domain, 'port': n.port, 'banner': n.banner,
                          'created': n.created.strftime("%Y-%m-%d %H:%M:%S")})
                ))
            )
        return nobita_list


class ShizukaManagement:

    def create(self, **kwargs):
        try:
            shi = Shizuka(ip=kwargs['data']['ip'], target=kwargs['data']['target'], domain=kwargs['data']['domain'])
            shi.save()
            return shi.id
        except errors.NotUniqueError as e:
            pass
        except errors.OperationError as e:
            print("[Shizuka in Views]")
            print("Exception", e)
        except Exception as e:
            print("[Shizuka in Views]")
            print("Exception", e)

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
        try:
            su = Suneo(ip=kwargs['data']['ip'], domain=kwargs['data']['domain'], cms=kwargs['data']['cms'],
                       technologies=kwargs['data']['technologies'])
            su.save()
            return su.id
        except errors.NotUniqueError as err:
            pass
        except Exception as e:
            print("[Suneo in Views]")
            print("Exception", e)

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
        try:
            geo = GeoLocation(
                ip=kwargs['data']['ip'],
                domain=kwargs['data']['domain'],
                continent=kwargs['data']['continent'],
                country=kwargs['data']['country'],
                organization=kwargs['data']['organization'],
                latitude=kwargs['data']['latitude'],
                longitude=kwargs['data']['longitude'],
            )
            geo.save()
            return geo.id
        except errors.NotUniqueError:
            pass
        except Exception as e:
            print("[GeoLocation in Views]")
            print("Exception", e)

    def get_geo(self, **kwargs):
        try:
            for g in GeoLocation.objects(domain=kwargs['domain']):
                return json.loads(JSONEncoder().encode(
                    dict({
                        'ip': g.ip, 'domain': g.domain, 'country': g.country, 'organization': g.organization,
                        'latitude': g.latitude, 'longitude': g.longitude
                    })
                ))
        except Exception as e:
            print("[GeoLocation in Views]")
            print("Exception", e)


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)
