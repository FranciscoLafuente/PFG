from cement import Controller, ex
import urllib.request as urllib
import re
import time
from bs4 import BeautifulSoup
from pymongo import MongoClient

TAG_RE = re.compile(r'<[^>]+>')
client = MongoClient('mongodb://localhost:27017/')
db = client.mydb
col = client.mydb.ipreverse


class Shizuka(Controller):
    class Meta:
        label = 'ipreverse'

    @ex(help='ip reverse de una ip dada',
        arguments=[
            (['-d', '--dir'],
             {'help': 'direccion ip a atacar',
              'dest': 'dir'})
        ]
        )
    def ipreverse(self):
        target = self.app.pargs.dir
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
                self.save_database(target, d)
                self.app.log.info(str(d) + " in " + str(target) + " already insert...")

    def remove_tags(self, text):
        return TAG_RE.sub('', text)

    def save_database(self, ip, domain):
        try:
            date_insert = time.strftime("%H:%M:%S")
            col.insert_one({"ip": ip, "domain": domain, "date_insert": date_insert})
        except:
            self.app.log.error("Error inserting to the mongodb")
