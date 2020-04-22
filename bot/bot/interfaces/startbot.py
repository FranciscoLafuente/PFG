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
    def send_nobita(self, data):
        """

        :param data:
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

    @abstractmethod
    def update_done(self, scan_id):
        """

        :param scan_id:
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
        self.app.log.info("Get scans by API")
        self.app.log.debug('about to greet end-user')
        type_bots, id_bot = self.login_bot()
        scans = self.stract_scans(id_bot)
        if not scans:
            self.app.log.info("There are not scans")
        return type_bots, scans

    def login_bot(self):
        token = self.app.config.get('bot', 'token')
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

    def send_nobita(self, data):
        response = requests.post("http://localhost:5000/bots/nobita", json=data,
                                 headers={'Authorization': 'Bearer ' + self.access_token})
        self.app.log.info("Nobita bot: " + response.json()['msg'])
        print()
        return

    def send_shizuka(self, data):
        response = requests.post("http://localhost:5000/bots/shizuka", json=data,
                                 headers={'Authorization': 'Bearer ' + self.access_token})
        self.app.log.info("Shizuka bot: " + response.json()['msg'])
        print()
        return

    def send_suneo(self, data):
        response = requests.post("http://localhost:5000/bots/suneo", json=data,
                                 headers={'Authorization': 'Bearer ' + self.access_token})
        self.app.log.info("Suneo bot: " + response.json()['msg'])
        print()

    def send_gigante(self, data):
        response = requests.post("http://localhost:5000/bots/gigante", json=data,
                                 headers={'Authorization': 'Bearer ' + self.access_token})
        self.app.log.info("Gigante bot: " + response.json()['msg'])
        print()

    def update_done(self, scan_id):
        response = requests.put("http://localhost:5000/bots/update_done/" + scan_id,
                                headers={'Authorization': 'Bearer ' + self.access_token})
        self.app.log.info("Updated DB: " + response.json()['msg'])
        print()
