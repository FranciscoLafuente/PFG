from .. import mongo
from ..models import time_str, JSONEncoder
import json
from bson import ObjectId


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
