from datetime import datetime
import json
from bson import ObjectId


def time_str():
    now = datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)
