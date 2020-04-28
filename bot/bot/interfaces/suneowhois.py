from abc import abstractmethod, ABC
from cement import Interface, Handler

import whois
# import ipwhois
import json
import urllib.request as urllib
from pprint import pprint


class SuneoWhoisInterface(Interface):
    class Meta:
        interface = 'suneowhoisIf'

    @abstractmethod
    def bot_scan(self, target):
        """

        :param target:
        :return:
        """
        pass


class SuneoWhoisHandler(SuneoWhoisInterface, Handler, ABC):
    class Meta:
        label = 'suneowhois'

    def __init__(self, **kw):
        super().__init__(**kw)
        self.response = []

    def bot_scan(self, target):
        self.app.log.info("BOT SUNEOWHOIS")
        self.app.log.info("Domain: " + target)
        w = whois.whois(target)
        pprint(w)
        name = w.org
        self.app.log.info("OWNER: " + name)
        try:
            url = "https://libreborme.net/borme/api/v1/persona/search/?q=" + str(name.replace(" ", "%20"))
            html = urllib.urlopen(url).read()
            data = json.loads(html)
            print("DATA", data)
            if data["objects"][0]["resource_uri"]:
                url = "https://libreborme.net" + data["objects"][0]["resource_uri"]
                html = urllib.urlopen(url).read()
                data = json.loads(html)
                lon_data = len(data["cargos_actuales"])
                for x in range(0, lon_data):
                    self.app.log.info("[URL TARGET] " + url)
                    self.app.log.info("Target Name: " + data["name"])
                    self.app.log.info("Business: " + data["cargos_actuales"][x]["name"])
                    self.app.log.info("Date From: " + data["cargos_actuales"][x]["date_from"])
                    self.app.log.info("Title: " + data["cargos_actuales"][x]["title"])
        except:
            pass
