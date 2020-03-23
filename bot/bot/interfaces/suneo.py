from abc import abstractmethod, ABC
from cement import Interface, Handler

import urllib
import re
import time
from bs4 import BeautifulSoup


class SuneoInterface(Interface):
    class Meta:
        interface = 'suneoIf'

    @abstractmethod
    def get_target(self, domain):
        """

        :param domain:
        :return:
        """
        pass


class SuneoHandler(SuneoInterface, Handler, ABC):
    class Meta:
        label = 'suneo'

    def __init__(self, **kw):
        super().__init__(**kw)
        self.response = []

    def get_target(self, domain):
        url = "http://" + domain
        user_agent = {'User-Agent': 'Mozilla 5.10'}
        request = urllib.request.Request(url, headers=user_agent)
        try:
            response = urllib.request.urlopen(request, timeout=10)
            if response.code == 200 or response.code == "OK":
                html = response.read()
                if self.detect_wp(html, domain):
                    self.response.append({'domain': domain, 'cms': 'wordpress'})
                if self.detect_joomla(html):
                    self.response.append({'domain': domain, 'cms': 'joomla'})
                if self.detect_drupal(html):
                    self.response.append({'domain': domain, 'cms': 'drupal'})

            print("Response", self.response)
        except urllib.error.URLError:
            pass
        except:
            pass

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
