from mongoengine import *
import datetime

connect('shoditaV2')


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


class ScansData(DynamicDocument):
    scan_user = ObjectIdField(required=True)
    results = ListField()
    created = DateTimeField(default=datetime.datetime.utcnow)


class MyBots(Document):
    name = StringField(required=True, unique=True)
    email = EmailField(required=True)
    ip = StringField(required=True)
    type = ListField(required=True)
    token = StringField()
    created = DateTimeField(default=datetime.datetime.utcnow)


class Nobita(Document):
    bot = StringField(default="nobita")
    ip = StringField()
    domain = StringField()
    port = IntField()
    banner = StringField()
    created = DateTimeField(default=datetime.datetime.utcnow)
    updated = DateTimeField()


class Shizuka(Document):
    bot = StringField(default="shizuka")
    ip = StringField()
    target = StringField()
    domain = StringField(unique=True)
    created = DateTimeField(default=datetime.datetime.utcnow)
    updated = StringField()


class Suneo(Document):
    bot = StringField(default="suneo")
    ip = StringField()
    domain = StringField(unique=True)
    cms = StringField()
    technologies = ListField()
    created = DateTimeField(default=datetime.datetime.utcnow)
    updated = StringField()


class Gigante(Document):
    bot = StringField(default="gigante")
    ip = StringField()
    domain = StringField()
    created = DateTimeField(default=datetime.datetime.utcnow)
    updated = StringField()


class GeoLocation(Document):
    ip = StringField(unique=True)
    domain = StringField(unique=True)
    continent = StringField()
    country = StringField()
    organization = StringField()
    latitude = FloatField()
    longitude = FloatField()
    created = DateTimeField(default=datetime.datetime.utcnow)
