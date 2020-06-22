from abc import abstractmethod, ABC
from cement import Interface, Handler

import urllib.request as urllib
import re
import time
from bs4 import BeautifulSoup
import socket


class ShizukaInterface(Interface):
    class Meta:
        interface = 'shizukaIf'

    @abstractmethod
    def bot_scan(self, *args):
        """
        This bot does ipreverse about a host.
        :return: A list with all information
        """
        pass


class ShizukaHandler(ShizukaInterface, Handler, ABC):
    class Meta:
        label = 'shizuka'

    def __init__(self, **kw):
        super().__init__(**kw)
        self.results = []

    def bot_scan(self, *args):
        target = args[0]
        ip = args[1]
        url = "https://www.robtex.net/?dns=" + str(target) + "&rev=1"
        req = urllib.Request(url, headers={'User-Agent': "Magic Browser"})
        html = urllib.urlopen(req).read()
        soup = BeautifulSoup(html, features="html.parser")

        table = soup.find_all("td")
        table = self.__remove_tags(str(table))
        data = table.split(",")
        for d in data:
            if len(d) > 10:
                d = d.replace("[", "")
                d = d.replace(" ", "")
                d = d.replace("]", "")
                self.results.append(d)

        return self.results

    def __remove_tags(self, text):
        TAG_RE = re.compile(r'<[^>]+>')
        return TAG_RE.sub('', text)
