from abc import abstractmethod, ABC
from cement import Interface, Handler
import requests
import jwt
import base64

RUTA = '/home/fran/Escritorio/Proyecto/PFG/bot/bot/interfaces/'


class ManageInterface(Interface):
    class Meta:
        interface = 'manageIf'

    @abstractmethod
    def download_files(self):
        """

        :return:
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
        :param kwargs:
        :return:
        """

    @abstractmethod
    def send_geo(self, **kwargs):
        """

        :param kwargs:
        :return:
        """

    @abstractmethod
    def send_bot(self, **kwargs):
        """

        :param kwargs:
        :return:
        """

    @abstractmethod
    def update_done(self, scan_id):
        """

        :param scan_id:
        :return:
        """
        pass


class ManageHandler(ManageInterface, Handler, ABC):
    class Meta:
        label = 'manage'

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
        except Exception as e:
            self.app.log.error("[Login Bot] Exception when trying to login bot:", e)
            self.app.log.error(self.access_token['msg'])

    def download_files(self, **kwargs):
        response = requests.get("http://localhost:5000/download/" + kwargs['type_bot'],
                                headers={'Authorization': 'Bearer ' + self.access_token})
        open(RUTA + kwargs['type_bot'] + '.py', 'wb').write(response.content)

        return True

    def stract_scans(self, id_bot):
        response = requests.get("http://localhost:5000/bots/scans", headers={'Authorization': 'Bearer '
                                                                                              + self.access_token})
        return response.json()

    def send_geo(self, **kwargs):
        self.app.log.info("Sending geo info to database...")
        try:
            response = requests.post("http://localhost:5000/bots/geo/" + kwargs['id'],
                                     json=kwargs['data'], headers={'Authorization': 'Bearer ' + self.access_token})
            self.app.log.info("Save in database")
            return response.json()
        except Exception as e:
            self.app.log.error("[Send Geo] Exception when sending data:", e)

    def send_data(self, **kwargs):
        self.app.log.info("Sending data to database...")
        try:
            response = requests.post("http://localhost:5000/bots/data/" + kwargs['id'], json=kwargs['data'],
                                     headers={'Authorization': 'Bearer ' + self.access_token})
            self.app.log.info("Backend response: " + response.json()['msg'])
        except Exception as e:
            self.app.log.error("[Send Data] Exception when sending data:", e)

    def send_bot(self, **kwargs):
        self.app.log.info("Sending data to database...")
        try:
            response = requests.post("http://localhost:5000/bots/" + kwargs['bot'] + "/" + kwargs['domain'] + "/" +
                                     kwargs['id'], json=kwargs['data'], headers={'Authorization': 'Bearer ' +
                                                                                                  self.access_token})
            self.app.log.info("Backend response: " + response.json()['msg'])
        except Exception as e:
            self.app.log.error("[Send Bot] Exception when sending data:", e)

    def update_done(self, scan_id):
        try:
            response = requests.put("http://localhost:5000/bots/update_done/" + scan_id,
                                    headers={'Authorization': 'Bearer ' + self.access_token})
            self.app.log.info("Updated DB: " + response.json()['msg'])
            print()
        except Exception as e:
            self.app.log.error("[Update Done] Exception when update field done:", e)
