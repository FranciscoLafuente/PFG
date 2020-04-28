from abc import abstractmethod, ABC
from cement import Interface, Handler

import urllib.request as urllib
import re
import time
from bs4 import BeautifulSoup
import socket


class ShiInterface(Interface):
    class Meta:
        interface = 'shiIf'

    @abstractmethod
    def ipreverse(self, target):
        """

        :param target:
        :return:
        """
        pass

    @abstractmethod
    def remove_tags(self, text):
        """

        :param text:
        :return:
        """
        pass


class ShiHandler(ShiInterface, Handler, ABC):
    class Meta:
        label = 'shi'

    def __init__(self, **kw):
        super().__init__(**kw)
        self.response = []

    def ipreverse(self, target):
        try:
            ip = socket.gethostbyname(target)
        except socket.gaierror as e:
            print(e)
            return

        url = 'https://viewdns.info/reverseip/?host=' + target + '&t=1'

        self.app.log.info("Obtaining the associated domains of " + target + "\n")

        req = urllib.Request(url, headers={'User-Agent': "Magic Browser"})
        html = urllib.urlopen(req).read()
        soup = BeautifulSoup(html, features="html.parser")

        table = soup.find_all("td")
        table = self.remove_tags(str(table))
        data = table.split(",")
        for d in data:
            if len(d) > 50 or d.find(".") < 0:
                pass
            else:
                self.response.append({'ip': ip, 'target': target, 'domain': d})

        return self.response

    def remove_tags(self, text):
        TAG_RE = re.compile(r'<[^>]+>')
        return TAG_RE.sub('', text)
