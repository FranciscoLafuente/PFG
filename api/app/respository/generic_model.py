from app import mongo
import datetime
from bson import ObjectId
import json


class Generic:

    def create(self, **kwargs):
        try:
            collection = mongo.db[kwargs['name']]
            id = collection.insert({
                'bot': kwargs['data']['bot'],
                'ip': kwargs['data']['ip'],
                'domain': kwargs['data']['domain'],
                'results': kwargs['data']['results'],
                'created': datetime.datetime.utcnow()
            })
            return id
        except Exception as e:
            print("[Create in Generic Collection]")
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
            print("[Create in Generic Collection]")
            print("Exception", e)


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)
