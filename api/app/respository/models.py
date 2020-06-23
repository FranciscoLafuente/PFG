from mongoengine import *
import datetime


class User(Document):
    email = EmailField(required=True, unique=True)
    name = StringField(required=True)
    password = StringField(required=True)
    projects = ListField()
    created = DateTimeField(default=datetime.datetime.utcnow)
    updated = DateTimeField(required=False)


class Project(Document):
    name = StringField(required=True, unique=True)
    type = BooleanField(default=False, required=True)  # If is public
    scans = ListField()
    created = DateTimeField(default=datetime.datetime.utcnow)


class Scan(Document):
    name = StringField(required=True, unique=True)
    hosts = ListField(required=True)
    bot = ObjectIdField()
    executionTime = DateTimeField(default=datetime.datetime.utcnow)
    created = DateTimeField(default=datetime.datetime.utcnow)
    done = BooleanField(default=False, required=True)
    launch = BooleanField(default=True, required=True)


class ScansData(DynamicDocument):
    scan_user = ObjectIdField(required=True)
    results = ListField()
    created = DateTimeField(default=datetime.datetime.utcnow)
    meta = {
        'ordering': ['-created']
    }


class MyBots(Document):
    name = StringField(required=True, unique=True)
    email = EmailField(required=True)
    ip = StringField(required=True)
    type = ListField(required=True)
    token = StringField()
    created = DateTimeField(default=datetime.datetime.utcnow)


class Bots(Document):
    name = StringField(required=True)
    description = StringField(required=True)
    created = DateTimeField(default=datetime.datetime.utcnow)