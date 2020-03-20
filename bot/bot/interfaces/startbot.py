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
        token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiI1YWEzMTNhYS02ODg0LTRhOTctOTZiZC03NGJhYzZjNGQwZTgiLCJmcmVzaCI6ZmFsc2UsImlhdCI6MTU4NDYyOTUxMiwidHlwZSI6ImFjY2VzcyIsIm5iZiI6MTU4NDYyOTUxMiwiaWRlbnRpdHkiOiI1ZTZlNWRmNThjOGI4NDQ1YzMxZDFlMTEifQ.xdkLvW3Z0b4HkzwMiELgKEBg_wMZRqFp4WuYZB_aBBA"
        # Get token bot
        response = requests.post("http://localhost:5000/bots/login", headers={'Authorization': 'Bearer ' + token})

        self.access_token = response.json()
        token_decode = jwt.decode(response.json(), verify=False)
        type_bots = token_decode['user_claims']
        id_bot = token_decode['identity']

        return type_bots, id_bot

    def stract_scans(self, id_bot):
        response = requests.get("http://localhost:5000/bots/scans", headers={'Authorization': 'Bearer '
                                                                                              + self.access_token})

        return response.json()
