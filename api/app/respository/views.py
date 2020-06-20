from werkzeug.security import generate_password_hash, check_password_hash
from .models import User, Project, Scan, ScansData, MyBots, Bots
import json
from bson import ObjectId
import datetime
from mongoengine import errors
from mongoengine.queryset.visitor import Q
from app.methods import JSONEncoder


class UserManagement:

    def create(self, data):
        try:
            password = self.password(data['password'])
            u = User(email=data['email'], name=data['name'], password=password)
            u.save()
            return True
        except errors.NotUniqueError:
            return False
        except Exception as e:
            print("[UserManagement - Create]")
            print("Exception", e)

    def change_password(self, **kwargs):
        try:
            password = self.password(kwargs['password'])
            for user in User.objects(email=kwargs['email']):
                User.objects(email=user.email).update_one(set__password=password)
                return True
            return False
        except Exception as e:
            print("[UserManagement - Change Password]")
            print("Exception", e)

    def exists(self, **kwargs):
        try:
            for user in User.objects(email=kwargs['email']):
                return user.email
        except Exception as e:
            print("[UserManagement - Exists]")
            print("Exception", e)

    def check(self, **kwargs):
        try:
            for user in User.objects(email=kwargs['email']):
                return check_password_hash(user.password, kwargs['password'])
            return False
        except Exception as e:
            print("[UserManagement - Check]")
            print("Exception", e)

    def add_project(self, **kwargs):
        try:
            for user in User.objects(email=kwargs['user']):
                User.objects(id=user.id).update(push__projects=kwargs['id'])
                return True
        except Exception as e:
            print("[UserManagement - Add Project]")
            print("Exception", e)

    def update_projects(self, **kwargs):
        try:
            for user in User.objects(email=kwargs['email']):
                User.objects(id=user.id).update(set__projects=kwargs['projects'])
                return True
        except Exception as e:
            print("[UserManagement - Update Projects]")
            print("Exception", e)

    def projects_id(self, **kwargs):
        try:
            for user in User.objects(email=kwargs['email']):
                return user.projects
        except Exception as e:
            print("[UserManagement - Projects Id]")
            print("Exception", e)

    def password(self, password):
        try:
            return generate_password_hash(password)
        except Exception as e:
            print("[UserManagement - Password]")
            print("Exception", e)


class ProjectManagement:

    def create(self, **kwargs):
        try:
            p = Project(name=kwargs['name'], type=kwargs['type'])
            p.save()
            return json.loads(JSONEncoder().encode(
                dict({'id': p.id, 'name': p.name, 'type': p.type})
            ))
        except errors.NotUniqueError:
            return False
        except Exception as e:
            print("[ProjectManagement - Create]")
            print("Exception", e)

    def project(self, **kwargs):
        try:
            for p in Project.objects(id=kwargs['id']):
                return json.loads(JSONEncoder().encode(
                    dict({'id': p.id, 'name': p.name, 'type': p.type, 'scans': p.scans})
                ))
        except Exception as e:
            print("[ProjectManagement - Project]")
            print("Exception", e)

    def add_scan(self, **kwargs):
        try:
            for p in Project.objects(id=kwargs['id']):
                Project.objects(id=p.id).update(push__scans=kwargs['scan_id'])
                return True
        except Exception as e:
            print("[ProjectManagement - Add Scan]")
            print("Exception", e)

    def scans_id(self, **kwargs):
        try:
            for p in Project.objects(id=kwargs['id']):
                return p.scans
        except Exception as e:
            print("[ProjectManagement - Scans Id]")
            print("Exception", e)

    def delete(self, **kwargs):
        try:
            Project.objects(id=kwargs['id']).delete()
        except Exception as e:
            print("[ProjectManagement - Delete]")
            print("Exception", e)

    def update_scans(self, **kwargs):
        try:
            for p in Project.objects(id=kwargs['id']):
                Project.objects(id=p.id).update(set__scans=kwargs['scans'])
                return True
        except Exception as e:
            print("[ProjectManagement - Update Scans]")
            print("Exception", e)


class ScanManagement:

    def create(self, **kwargs):
        try:
            if kwargs['execution_time']:
                s = Scan(name=kwargs['name'], hosts=kwargs['hosts'], bot=kwargs['bot'],
                         executionTime=kwargs['execution_time'])
            else:
                s = Scan(name=kwargs['name'], hosts=kwargs['hosts'], bot=kwargs['bot'])
            s.save()
            return s.id
        except errors.NotUniqueError:
            return False
        except Exception as e:
            print("[ScanManagement - Create]")
            print("Exception", e)

    def get_scan(self, **kwargs):
        try:
            for s in Scan.objects(id=kwargs['id']):
                return json.loads(JSONEncoder().encode(
                    dict({'id': s.id, 'name': s.name, 'hosts': s.hosts,
                          'executionTime': s.executionTime.strftime("%Y-%m-%d %H:%M:%S"),
                          'created': s.created.strftime("%Y-%m-%d %H:%M:%S"),
                          'done': s.done, 'launch': s.launch})
                ))
        except Exception as e:
            print("[ScanManagement - Get Scan]")
            print("Exception", e)

    def change_launch(self, **kwargs):
        try:
            for s in Scan.objects(id=kwargs['id']):
                Scan.objects(id=s.id).update(set__launch=kwargs['value'])
        except Exception as e:
            print("[ScanManagement - Change Launch]")
            print("Exception", e)

    def change_done(self, **kwargs):
        try:
            for s in Scan.objects(id=kwargs['id']):
                Scan.objects(id=s.id).update(set__done=kwargs['value'])
        except Exception as e:
            print("[ScanManagement - Change Done]")
            print("Exception", e)

    def cahnge_bot(self, **kwargs):
        try:
            for s in Scan.objects(id=kwargs['id']):
                Scan.objects(id=s.id).update(set__bot=kwargs['bot'])
        except Exception as e:
            print("[ScanManagement - Change Bot]")
            print("Exception", e)

    def delete(self, **kwargs):
        try:
            Scan.objects(id=kwargs['id']).delete()
        except Exception as e:
            print("[ScanManagement - Delete]")
            print("Exception", e)

    def scans_by_bot(self, **kwargs):
        try:
            scans_list = []
            for s in Scan.objects(bot=ObjectId(kwargs['bot'])):
                scans_list.append(
                    json.loads(JSONEncoder().encode(
                        dict({'id': s.id, 'hosts': s.hosts,
                              'executionTime': s.executionTime.strftime("%Y-%m-%d %H:%M:%S"),
                              'done': s.done, 'launch': s.launch})
                    )))
            return scans_list
        except Exception as e:
            print("[ScanManagement - Scans By Bot]")
            print("Exception", e)


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
            print('[ScansData - Get Scans]')
            print('Exception', e)

    def get_scans_pag(self, **kwargs):
        list_scans = []
        try:
            for s in ScansData.objects[kwargs['page']:kwargs['size']](scan_user=kwargs['scan'],
                                                                      domain=kwargs['domain']):
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
            print('[ScansData - Get Scans Paginated]')
            print('Exception', e)

    def scans_items(self, **kwargs):
        items = 0
        try:
            for _ in ScansData.objects(scan_user=kwargs['scan'], domain=kwargs['domain']):
                items += 1
            return items
        except Exception as e:
            print('[ScansData - Scans Items]')
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
            print('ScansData - One Scan')
            print('Exception', e)

    def search(self, **kwargs):
        list_scans = []
        try:
            for s in ScansData.objects[kwargs['start']:kwargs['end']](
                    Q(continent__icontains=kwargs['searchText']) | Q(country__icontains=kwargs['searchText'])
                    | Q(organization__icontains=kwargs['searchText']) | Q(domain__icontains=kwargs['searchText'])
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
            print('[ScansData - Search]')
            print('Exception', e)

    def searchItems(self, **kwargs):
        items = 0
        try:
            for _ in ScansData.objects(
                    Q(continent__icontains=kwargs['searchText']) | Q(country__icontains=kwargs['searchText'])
                    | Q(organization__icontains=kwargs['searchText']) | Q(domain__icontains=kwargs['searchText'])
            ):
                items += 1
            return items
        except Exception as e:
            print('[ScansData - Search Items]')
            print('Exception', e)


class MyBotsManagement:

    def create(self, **kwargs):
        try:
            b = MyBots(name=kwargs['name'], email=kwargs['email'], ip=kwargs['ip'], type=kwargs['type'])
            b.save()
            return json.loads(JSONEncoder().encode(
                dict({'id': b.id, 'ip': b.ip, 'name': b.name, 'type': b.type})
            ))
        except errors.NotUniqueError:
            return False
        except Exception as e:
            print('[MyBots - Create]')
            print('Exception', e)

    def get_id(self, **kwargs):
        try:
            for b in MyBots.objects(name=kwargs['name']):
                return b.id
        except Exception as e:
            print('[MyBots - Get Id]')
            print('Exception', e)

    def get_bots(self, **kwargs):
        try:
            list_bots = []
            for b in MyBots.objects(email=kwargs['email']):
                list_bots.append(
                    json.loads(JSONEncoder().encode(
                        dict({'id': b.id, 'ip': b.ip, 'name': b.name, 'type': b.type, 'token': b.token})
                    )))
            return list_bots
        except Exception as e:
            print('[MyBots - Get Bots]')
            print('Exception', e)

    def get_all_bots(self):
        try:
            list_bots = []
            for b in MyBots.objects:
                list_bots.append(
                    json.loads(JSONEncoder().encode(
                        dict({'id': b.id, 'ip': b.ip, 'name': b.name, 'type': b.type, 'token': b.token})
                    )))
            return list_bots
        except Exception as e:
            print('[MyBots - Get All Bots]')
            print('Exception', e)

    def add_token(self, **kwargs):
        try:
            for b in MyBots.objects(id=kwargs['id']):
                MyBots.objects(id=b.id).update(set__token=kwargs['token'])
        except Exception as e:
            print('[MyBots - Add Token]')
            print('Exception', e)

    def delete(self, **kwargs):
        try:
            MyBots.objects(id=kwargs['id']).delete()
        except Exception as e:
            print('[MyBots - Delete]')
            print('Exception', e)

    def search_bot(self, **kwargs):
        try:
            for b in MyBots.objects(id=kwargs['id'], ip=kwargs['ip']):
                return b.type
        except Exception as e:
            print('[MyBots - Search Bot]')
            print('Exception', e)


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
            print("[Bots - Create]")
            print("Exception", e)

    def get(self):
        try:
            list_bots = []
            for b in Bots.objects:
                list_bots.append(b.name)
            return list_bots
        except Exception as e:
            print("[Bots - Get]")
            print("Exception", e)
