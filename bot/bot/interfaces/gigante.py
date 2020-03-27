from abc import abstractmethod, ABC
from cement import Interface, Handler

import time
import socket
import paramiko


class GiganteInterface(Interface):
    class Meta:
        interface = 'giganteIf'

    @abstractmethod
    def check_ssh(self, target):
        """
        Check if the passwords are valid
        :param target: The ip to check
        :return: The ip
        """
        pass


class GiganteHandler(GiganteInterface, Handler, ABC):
    class Meta:
        label = 'gigante'

    def __init__(self, **kw):
        super().__init__(**kw)
        self.passwords = ["123456", "root", "admin", "12345"]
        self.response = ""

    def check_ssh(self, target):
        paramiko.util.log_to_file("filename.log")
        fail = 0
        user = "root"
        for p in self.passwords:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            try:
                self.app.log.info("Try user: root password: " + p)
                ssh.connect(target, username=user, password=p, timeout=10)
            except paramiko.AuthenticationException as error:
                self.app.log.info("Incorrect password... root@" + target + ":" + p)
                continue
            except socket.error as error:
                fail += 1
                print(error)
                continue
            except paramiko.SSHException as error:
                fail += 1
                print(error)
                self.app.log.info("Most probably this is caused by a missing host key")
                continue
            except Exception as error:
                fail += 1
                self.app.log.info("Unknown error: " + str(error))
                continue
            except:
                fail += 1
            ssh.close()
        if fail == 0:
            self.app.log.info(target + " has a brute force vulnerability in SSH...")
            # insert_mongodb(target)
        else:
            self.app.log.info(target + " is protected...")
