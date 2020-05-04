from app import mongo
import datetime
from bson import ObjectId
import json
from bson.json_util import dumps


class Generic:

    def create(self, **kwargs):
        try:
            collection = mongo.db[kwargs['name']]
            id = collection.insert({
                'host': kwargs['host'],
                'id_scan': kwargs['id'],
                'results': kwargs['data'],
                'created': datetime.datetime.utcnow()
            })
            return id
        except Exception as e:
            print("[Create in Generic Collection]")
            print("Exception", e)

    def create_nobita(self, **kwargs):
        try:
            collection = mongo.db[kwargs['name']]
            id = collection.insert({
                'host': kwargs['host'],
                'id_scan': kwargs['id'],
                'port': kwargs['data']['port'],
                'banner': kwargs['data']['banner'],
                'created': datetime.datetime.utcnow()
            })
            return id
        except Exception as e:
            print("[CreateNobita in Generic Collection]")
            print("Exception", e)

    def read(self, **kwargs):
        try:
            collection = mongo.db[kwargs['name']]
            res = collection.find_one({
                '_id': ObjectId(kwargs['id']),
            })
            res['created'] = res['created'].strftime("%Y-%m-%d %H:%M:%S")
            return json.loads(JSONEncoder().encode(res))
        except Exception as e:
            print("[Read in Generic Collection]")
            print("Exception", e)

    def search(self, **kwargs):
        try:
            collection = mongo.db[kwargs['collection']]
            res = collection.find_one({
                'port': int(kwargs['port']),
            })
            return res['id_scan']
        except Exception as e:
            print("[Search in Generic Collection]")
            print("Exception", e)


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)
