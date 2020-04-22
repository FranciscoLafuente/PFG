from abc import abstractmethod, ABC
from cement import Interface, Handler

import json
from bson import ObjectId
import builtwith
import socket
from pprint import pprint


class SuneoV2Interface(Interface):
    class Meta:
        interface = 'suneoV2If'

    @abstractmethod
    def get_cms(self, domain, ip):
        """"""
        pass


class SuneoV2Handler(SuneoV2Interface, Handler, ABC):
    class Meta:
        label = 'suneoV2'

    def __init__(self, **kw):
        super().__init__(**kw)

    def get_cms(self, domain, ip):
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
        return json.loads(JSONEncoder().encode({'ip': ip, 'domain': domain, 'cms': cms,
                                                'technologies': list(set(technologies))}))


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)
