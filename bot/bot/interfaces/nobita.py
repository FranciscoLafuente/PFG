from abc import abstractmethod, ABC
from cement import Interface, Handler
from pymongo import MongoClient

import socket
import threading
import ssl
from queue import Queue

client = MongoClient('mongodb://localhost:27017/')
db = client.mydb
col = client.mydb.port_scanner


class NobitaInterface(Interface):
    class Meta:
        interface = 'nobita'

    @abstractmethod
    def pscan(self, ip_address):
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
    def save_database(self, port, banner):
        """"""
        pass

    @abstractmethod
    def format_text(self, text):
        """"""
        pass


class NobitaHandler(NobitaInterface, Handler, ABC):
    class Meta:
        label = 'portscan'

    def pscan(self, ip_address):
        queue = Queue()
        mode = 1
        self.get_ports(mode, queue)
        # Number of threads that you want to use
        threads = 600
        thread_list = []

        self.app.log.info('Scanning the ports of ' + ip_address)

        for t in range(threads):
            thread = threading.Thread(
                target=self.worker, args=(ip_address, queue,))
            thread.start()
            thread_list.append(thread)

        for thread in thread_list:
            thread.join()

        self.app.log.info("Scanning completed")

    def connect(self, ip_address, port):
        target = ip_address

        try:
            if port == 443:
                socketssl = socket.socket()
                socketssl.settimeout(3.0)
                s = ssl.wrap_socket(socketssl)
            else:
                s = socket.socket()
                s.settimeout(5.0)
            con = s.connect_ex((target, port))
            request = "GET / HTTP/1.1\nHost: " + ip_address + "\n\n"
            s.send(request.encode())
            banner = s.recv(1024)
            # If the response is 0, it's mean that the connection is succesfull
            if con is 0:
                self.save_database(port, self.format_text(str(banner)))
                s.close()
                return True
            s.close()
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
                print("[-] Port {} is open".format(port))

    def save_database(self, port, banner):
        try:
            col.insert_one({'port': port, 'banner': banner})
        except:
            self.app.log.error("Error inserting to the mongodb")

    def format_text(self, text):
        text = str(text).replace('\\r\\n', "\n")
        text = text.lstrip("b'").rstrip("'")
        return text
