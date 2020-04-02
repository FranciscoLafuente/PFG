from .. import mongo
from ..models import time_str, JSONEncoder
import json
from bson import ObjectId


class Scan:

    def create_scan(self, user, id_project, name_scan, bots, hosts, executiontime):
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
            "executiontime": executiontime,
            "hosts": hosts,
            'created': time_str(),
            'done': False
        })

        # Update project with the new scan
        mongo.db.projects.update(
            {'_id': ObjectId(id_project)},
            {'$push': {"scans": new_scan}}
        )
        scan_created = mongo.db.scans.find_one({'_id': ObjectId(new_scan)})
        return json.loads(JSONEncoder().encode(scan_created))

    def get_scans(self, id_project):
        project = mongo.db.projects.find_one({'_id': ObjectId(id_project)})
        scans_project = project.get('scans')
        list_s = []
        for s in scans_project:
            scan = mongo.db.scans.find_one({'_id': ObjectId(s)})
            list_s.append(json.loads(JSONEncoder().encode(scan)))

        return list_s

    def get_scans_by_bot(self, id_bot):
        list_s = []
        for scan in mongo.db.scans.find({'bots': ObjectId(id_bot)}):
            list_s.append(json.loads(JSONEncoder().encode(scan)))

        return list_s

    def change_done(self, scan_id):
        update = mongo.db.scans.update(
            {'_id': ObjectId(scan_id)},
            {'$set': {"done": True}}
        )
        return update

    def update_scan_bots(self, scan, id_bot):
        list_update = []
        bot_str = JSONEncoder().encode(id_bot)
        # Get all bots in a specific scan
        bots = scan['bots']
        for b in bots:
            b_str = JSONEncoder().encode(b)
            if b_str != bot_str:
                list_update.append(b)

        update = mongo.db.scans.update(
            {'_id': ObjectId(scan['_id'])},
            {'$set': {"bots": list_update}}
        )
        return update
