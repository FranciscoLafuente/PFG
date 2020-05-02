from abc import abstractmethod, ABC
from cement import Interface, Handler

import json
from bson import ObjectId
import builtwith
import socket
from pprint import pprint


class SuneoInterface(Interface):
    class Meta:
        interface = 'suneoIf'

    @abstractmethod
    def bot_scan(self, *args):
        """"""
        pass


class SuneoHandler(SuneoInterface, Handler, ABC):
    class Meta:
        label = 'suneo'

    def __init__(self, **kw):
        super().__init__(**kw)

    def bot_scan(self, *args):
        domain = args[0]
        ip = args[1]
        try:
            website = builtwith.parse('https://' + domain)
        except UnicodeDecodeError:
            return {}
        # Check if cms exists
        cms = ""
        if 'cms' in website.keys():
            cms = website['cms'][0]
        # Get all technologies
        technologies = []
        for value in website.values():
            for e in value:
                technologies.append(e)
        # Technologies without duplicates elements
        r = dict({'cms': cms, 'technologies': list(set(technologies))})
        return [r]


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)
