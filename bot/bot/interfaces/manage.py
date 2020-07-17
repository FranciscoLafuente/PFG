from abc import abstractmethod, ABC
from cement import Interface, Handler
import requests
import jwt
import base64
import sys

class ManageInterface(Interface):
    class Meta:
        interface = 'manageIf'

    @abstractmethod
    def download_files(self):
        """
        Download all bots files from the API
        :return: The bots files
        """

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
        When the bot does login
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
    def send_data(self, **kwargs):
        """
        Send to API all information getting
        :param kwargs:
        :return: A object with all information
        """

    @abstractmethod
    def update_done(self, scan_id):
        """
        Request to API to change value done to true, in a scan
        :param scan_id: Scan id
        :return: Print the message responsed from the API
        """
        pass


class ManageHandler(ManageInterface, Handler, ABC):
    class Meta:
        label = 'manage'

    def __init__(self, **kw):
        super().__init__(**kw)
        self.url = ""
        self.access_token = ""

    def get_scan(self):
        self.url = self.app.config.get('url', 'dev')
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
            response = requests.post(self.url + "bots/login", headers={'Authorization': 'Bearer ' + token})
            self.access_token = response.json()
            token_decode = jwt.decode(response.json(), verify=False)
            type_bots = token_decode['user_claims']
            id_bot = token_decode['identity']

            return type_bots, id_bot
        except Exception as e:
            self.app.log.error("[Login Bot] Exception when trying to login bot:", e)
            self.app.log.error(self.access_token['msg'])
            sys.exit(1)

    def download_files(self, **kwargs):
        try:
            route = self.app.config.get('route', 'store_files')
            response = requests.get(self.url + "download/" + kwargs['type_bot'],
                                    headers={'Authorization': 'Bearer ' + self.access_token})
            open(route + kwargs['type_bot'] + '.py', 'wb').write(response.content)

            return True
        except Exception as e:
            self.app.log.error("[Download Files] Exception when trying download bots:", e)
            self.app.log.error(self.access_token['msg'])

    def stract_scans(self, id_bot):
        response = requests.get(self.url + "bots/scans", headers={'Authorization': 'Bearer '
                                                                                   + self.access_token})
        return response.json()

    def send_data(self, **kwargs):
        self.app.log.info("Sending data to database...")
        try:
            response = requests.post(self.url + "bots/data/" + kwargs['id'], json=kwargs['data'],
                                     headers={'Authorization': 'Bearer ' + self.access_token})
            self.app.log.info("Backend response: " + response.json()['msg'])
        except Exception as e:
            self.app.log.error("[Send Data] Exception when sending data:", e)

    def update_done(self, scan_id):
        try:
            response = requests.put(self.url + "bots/update_done/" + scan_id,
                                    headers={'Authorization': 'Bearer ' + self.access_token})
            self.app.log.info("Updated DB: " + response.json()['msg'])
            print()
        except Exception as e:
            self.app.log.error("[Update Done] Exception when update field done:", e)
