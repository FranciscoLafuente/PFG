from abc import abstractmethod, ABC
from cement import Interface, Handler

import socket
import threading
import ssl
import requests
import json
from queue import Queue


class NobitaInterface(Interface):
    class Meta:
        interface = 'nobitaIf'

    @abstractmethod
    def pscan(self, address, ip_address):
        """"""
        pass

    @abstractmethod
    def connect(self, ip_address, port):
        """"""
        pass

    @abstractmethod
    def get_ports(self, mode, queue):
        """"""
        pass

    @abstractmethod
    def worker(self, target, queue):
        """"""
        pass

    @abstractmethod
    def save_scan(self, ip_address, port, result):
        """"""
        pass

    @abstractmethod
    def format_text(self, text):
        """"""
        pass

    @abstractmethod
    def geo_ip(self, ip):
        """"""
        pass


class NobitaHandler(NobitaInterface, Handler, ABC):
    class Meta:
        label = 'nobita'

    def __init__(self, **kw):
        super().__init__(**kw)
        self.port_scanner = []
        self.domain = ""

    def pscan(self, address, ip_address):
        self.domain = address

        queue = Queue()
        mode = 3
        self.get_ports(mode, queue)
        # Number of threads that you want to use
        threads = 30
        thread_list = []

        self.app.log.info('Scanning the ports of ' + ip_address)

        for t in range(threads):
            thread = threading.Thread(
                target=self.worker, args=(ip_address, queue,))
            thread.start()
            thread_list.append(thread)

        for thread in thread_list:
            thread.join()

        return self.port_scanner

    def connect(self, ip_address, port):
        target = ip_address
        socket.setdefaulttimeout(5.0)

        try:
            if port == 443:
                socketssl = socket.socket()
                s = ssl.wrap_socket(socketssl)
            else:
                s = socket.socket()
            con = s.connect_ex((target, port))
            request = "GET / HTTP/1.1\nHost: " + ip_address + "\n\n"
            s.send(request.encode())
            result = s.recv(1024)
            s.close()

            # Print results
            json_obj = result.decode('utf8').replace("'", '"')
            banner = self.format_text(json_obj)
            # If the response is 0, it's mean that the connection is succesfull
            if con is 0:
                self.save_scan(ip_address, port, banner)
                return True
            return False
        except:
            return False

    def get_ports(self, mode, queue):
        if mode == 1:
            for port in range(1, 1024):
                queue.put(port)
        elif mode == 2:
            for port in range(1, 49125):
                queue.put(port)
        elif mode == 3:
            ports = [20, 21, 22, 23, 25, 53, 80, 110, 123, 443]
            for port in ports:
                queue.put(port)

    def worker(self, target, queue):
        while not queue.empty():
            port = queue.get()
            if self.connect(target, port):
                self.app.log.info("[-] Port {} is open".format(port))

    def geo_ip(self, ip):
        try:
            url = "http://ip-api.com/json/" + str(ip)
            response = requests.get(url)
            json_obj = response.json()
            return json_obj
        except:
            pass

    def save_scan(self, ip_address, port, result):
        self.port_scanner.append({'ip': ip_address, 'domain': self.domain, 'port': port, 'banner': result})

    def format_text(self, text):
        text = str(text).replace('\\r\\n', "\n")
        sep = '<'
        result = text.split(sep, 1)[0]
        return result
