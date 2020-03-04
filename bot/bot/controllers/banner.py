import socket
import ssl
import requests
import json
import sys
from cement import Controller, ex
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client.mydb
col = client.mydb.banner_grabbing


class Nobita(Controller):
    class Meta:
        label = 'banner'

    @ex(help='obtener banner',
        arguments=[
            (['-d', '--dir'],
             {'help': 'direccion ip a atacar',
              'dest': 'dir'}),
            (['-p', '--p'],
             {'help': 'puerto a atacar',
              'default': 80,
              'dest': 'port'})
        ],
        )
    def banner(self):
        ip_address = socket.gethostbyname(self.app.pargs.dir)
        port = int(self.app.pargs.port)

        self.app.log.info("Checking the port " + str(port) +
                          " in the ip " + str(ip_address) + "\n")

        try:
            if port in [80, 8080, 28017]:
                s = socket.socket()
                s.settimeout(3.0)
            elif port == 443:
                socketssl = socket.socket()
                socketssl.settimeout(3.0)
                s = ssl.wrap_socket(socketssl)

            s.connect_ex((ip_address, int(port)))
            msg = "GET / HTTP/1.1\r\nHost: " + ip_address + "\r\n\r\n"
            s.send(msg.encode())
            result = s.recv(5120)
            
            # Print the results
            json_obj = result.decode('utf8').replace("'", '"')
            banner = self.format_text(json_obj)
            print("[-] Banner Grabbing: \n" + banner)
            # Save in database with geolocation
            data_geoip = self.geo_ip(ip_address)
            if data_geoip is not None:
                self.insert_mongo(ip_address, port, banner, **data_geoip)
                self.app.log.info("The banner has been saved in the database\n")
        except:
            sys.exc_info()
            self.app.log.error(
                "It has been imposible to get the banner grabbing")
            return

    def save_file(self, text):
        try:
            file = open("data/datos.txt", "a", encoding="utf-8")
            s = str(text)
            file.write(s + "\n")
            file.close()
        except:
            self.app.log.error("Error saving to file")

    def format_text(self, text):
        text = str(text).replace('\\r\\n', "\n")
        sep = '<'
        result = text.split(sep, 1)[0]
        return result

    def geo_ip(self, ip):
        try:
            url = "http://ip-api.com/json/" + str(ip)
            response = requests.get(url)
            json_obj = response.json()
            return json_obj
        except:
            pass

    def insert_mongo(self, ip_address, port, result, **kwargs):
        try:
            col.insert_one({'ip_address': ip_address, 'country': kwargs.get('country'),
                            'city': kwargs.get('city'), 'region_name': kwargs.get('regionName'), 'isp': kwargs.get('isp'),
                            'port': port, 'banner': result, 'latitud': kwargs.get('lat'),
                            'longitud': kwargs.get('lon'), 'zip': kwargs.get('zip'), 'bot': 'Nobita', })
        except:
            self.app.log.error("Error inserting to the mongodb")
