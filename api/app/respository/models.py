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
    type = BooleanField(required=True)  # If is public
    scans = ListField()
    created = DateTimeField(default=datetime.datetime.utcnow)


class Scan(Document):
    name = StringField(required=True, unique=True)
    hosts = StringField(required=True)
    bot = ObjectIdField()
    executionTime = DateTimeField()
    created = DateTimeField(default=datetime.datetime.utcnow)
    done = BooleanField(default=False, required=True)


class Bot(Document):
    name = StringField(required=True, unique=True)
    email = EmailField(required=True)
    ip = StringField(required=True)
    type = ListField(required=True)
    token = StringField()
    created = DateTimeField(default=datetime.datetime.utcnow)


class Nobita(Document):
    bot = StringField(default="nobita")
    ip_address = StringField()
    domain = StringField()
    port = IntField()
    created = DateTimeField(default=datetime.datetime.utcnow)
    updated = DateTimeField()
    banner = StringField()
    country = StringField()
    city = StringField()
    region_name = StringField()
    isp = StringField()
    latitud = FloatField()
    longitud = FloatField()
    zip = StringField()


class Shizuka(Document):
    bot = StringField(default="shizuka")
    ip = StringField()
    target = StringField()
    domain = StringField()
    created = DateTimeField(default=datetime.datetime.utcnow)
    updated = StringField()


class Suneo(Document):
    bot = StringField(default="suneo")
    ip = StringField()
    domain = StringField()
    cms = StringField()
    created = DateTimeField(default=datetime.datetime.utcnow)
    updated = StringField()


class Gigante(Document):
    bot = StringField(default="gigante")
    ip = StringField()
    domain = StringField()
    created = DateTimeField(default=datetime.datetime.utcnow)
    updated = StringField()
