from abc import abstractmethod, ABC
from cement import Interface, Handler
import requests
import jwt
import base64


class ScansInterface(Interface):
    class Meta:
        interface = 'startbot'

    @abstractmethod
    def get_scan(self):
        """
        Start scans with the selected bot.

        :return: if the scan has been succesfull
        """
        pass

    @abstractmethod
    def login_bot(self):
        """
        :return: The type of bots
        """
        pass

    @abstractmethod
    def stract_scans(self, projects):
        """
        Get all scans of given projects
        :param projects: The user projects
        :return: The list of scans
        """
        pass

    @abstractmethod
    def send_nobita(self, scan):
        """

        :param scan:
        :return:
        """
        pass

    @abstractmethod
    def send_shizuka(self, data):
        """

        :param data:
        :return:
        """
        pass

    @abstractmethod
    def send_suneo(self, data):
        """

        :param data:
        :return:
        """
        pass

    @abstractmethod
    def send_gigante(self, data):
        """

        :param data:
        :return:
        """
        pass


class ScansHandler(ScansInterface, Handler, ABC):
    class Meta:
        label = 'connect'

    def __init__(self, **kw):
        super().__init__(**kw)
        self.access_token = ""

    def get_scan(self):
        self.app.log.debug('about to greet end-user')
        type_bots, id_bot = self.login_bot()
        scans = self.stract_scans(id_bot)
        return type_bots, scans

    def login_bot(self):
        token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiI4Nzg0MDg2ZS1kYmZkLTRlMzItYjUxZC00OTUxYmFhODU2ZDYiLCJmcmVzaCI6ZmFsc2UsImlhdCI6MTU4NTMxMTM3MCwidHlwZSI6ImFjY2VzcyIsIm5iZiI6MTU4NTMxMTM3MCwiaWRlbnRpdHkiOiI1ZTdkZWU4NTZhM2I3MzdmZDllN2JkNWIifQ.1zsB14KNuDzz6uNLFyxQNgiFfW4pMBL1-HghgweYoVY"
        try:
            # Get token bot
            response = requests.post("http://localhost:5000/bots/login", headers={'Authorization': 'Bearer ' + token})
            self.access_token = response.json()
            token_decode = jwt.decode(response.json(), verify=False)
            type_bots = token_decode['user_claims']
            id_bot = token_decode['identity']

            return type_bots, id_bot
        except:
            self.app.log.error(self.access_token['msg'])

    def stract_scans(self, id_bot):
        response = requests.get("http://localhost:5000/bots/scans", headers={'Authorization': 'Bearer '
                                                                                              + self.access_token})
        return response.json()

    def send_nobita(self, scan, scan_id):
        response = requests.post("http://localhost:5000/bots/nobita/" + scan_id, json=scan,
                                 headers={'Authorization': 'Bearer ' + self.access_token})
        print(response.json()['msg'])

    def send_shizuka(self, data):
        response = requests.post("http://localhost:5000/bots/shizuka", json=data,
                                 headers={'Authorization': 'Bearer ' + self.access_token})
        print(response.json()['msg'])

    def send_suneo(self, data):
        response = requests.post("http://localhost:5000/bots/suneo", json=data,
                                 headers={'Authorization': 'Bearer ' + self.access_token})
        print(response.json()['msg'])

    def send_gigante(self, data):
        response = requests.post("http://localhost:5000/bots/gigante", json=data,
                                 headers={'Authorization': 'Bearer ' + self.access_token})
        print(response.json()['msg'])
