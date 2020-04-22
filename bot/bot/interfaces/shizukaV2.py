from abc import abstractmethod, ABC
from cement import Interface, Handler

import urllib.request as urllib
import re
import time
from bs4 import BeautifulSoup
import socket


class ShizukaV2Interface(Interface):
    class Meta:
        interface = 'shizukaV2If'

    @abstractmethod
    def get_domain(self, target, ip):
        """

        :param target:
        :return:
        """
        pass


class ShizukaV2Handler(ShizukaV2Interface, Handler, ABC):
    class Meta:
        label = 'shizukaV2'

    def __init__(self, **kw):
        super().__init__(**kw)
        self.response = []

    def get_domain(self, target, ip):
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
                self.response.append({'ip': ip, 'target': target, 'domain': d})

        return self.response

    def __remove_tags(self, text):
        TAG_RE = re.compile(r'<[^>]+>')
        return TAG_RE.sub('', text)
