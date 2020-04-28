from abc import abstractmethod, ABC
from cement import Interface, Handler

import urllib
import re
import time
from bs4 import BeautifulSoup
import socket


class SuInterface(Interface):
    class Meta:
        interface = 'suIf'

    @abstractmethod
    def get_target(self, domain):
        """

        :param domain:
        :return:
        """
        pass


class SuHandler(SuInterface, Handler, ABC):
    class Meta:
        label = 'su'

    def __init__(self, **kw):
        super().__init__(**kw)
        self.results = []
        self.ip = ""

    def get_target(self, domain):
        self.app.log.info("BOT SUNEO")
        try:
            self.ip = socket.gethostbyname(domain)
        except socket.gaierror as e:
            print(e)
            return

        url = "http://" + domain
        self.app.log.info("Generate URL: " + str(url))
        user_agent = {'User-Agent': 'Mozilla 5.10'}
        request = urllib.request.Request(url, headers=user_agent)
        try:
            response = urllib.request.urlopen(request, timeout=10)
            if response.code == 200 or response.code == "OK":
                html = response.read()
                if self.detect_wp(html, domain):
                    self.results.append({'cms': 'wordpress'})
                    self.app.log.info(domain + " is WordPress")
                if self.detect_joomla(html):
                    self.results.append({'cms': 'joomla'})
                    self.app.log.info(domain + " is Joomla")
                if self.detect_drupal(html):
                    self.results.append({'cms': 'drupal'})
                    self.app.log.info(domain + " is Drupal")

        except urllib.error.URLError:
            pass
        else:
            return {'bot': 'suneo', 'ip': ip_address, 'domain': domain, 'results': self.results}

    def detect_joomla(self, html):
        soup = BeautifulSoup(html, features="html.parser")
        # Buscamos el generator
        try:
            gen = soup.findAll(attrs={"name": "generator"})
            if "Joomla!" in str(gen):
                return True
        except:
            return False

    def detect_drupal(self, html):
        soup = BeautifulSoup(html, features="html.parser")
        # Buscamos el generator
        try:
            gen = soup.findAll(attrs={"name": "generator"})
            if "Drupal" in str(gen):
                return True
        except:
            return False

    def detect_wp(self, html, domain):
        soup = BeautifulSoup(html, features="html.parser")
        try:
            # Buscamos generator
            gen = soup.findAll(attrs={"name": "generator"})
            if "WordPress" in str(gen) or "Wordpress" in str(gen):
                return True
            else:  # Buscamos wp-content en el html
                if html.find("wp-content") > 0:
                    return True
                else:  # Buscamos links con xmlrpc.php
                    links = soup.findAll("link")
                    for l in links:
                        if "xmlrpc.php" in str(l):
                            return True
                        else:  # Buscamos el readme.html
                            try:
                                url = "http://" + domain + "/readme.html"
                                html = urllib.request.urlopen(url).read()
                                soup = BeautifulSoup(html)
                                for h1 in soup.find_all('h1', {'id': "logo"}):
                                    h1 = self.__remove_tags(str(h1))  # PARSER
                                    if h1:
                                        return True
                            except urllib.error.HTTPError as e:
                                continue
                            except urllib.error.URLError as e:
                                continue
        except:
            return False

    def __remove_tags(self, text):
        TAG_RE = re.compile(r'<[^>]+>')
        return TAG_RE.sub('', text)
