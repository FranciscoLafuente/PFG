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
    def get_projects(self):
        """
        Get all projects by especific user

        :return: The list of projects
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

    def get_scan(self):
        self.app.log.debug('about to greet end-user')
        projects = self.get_projects()
        self.stract_scans(projects)

    def get_projects(self):
        token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2NsYWltcyI6eyJwcm9qZWN0SWQiOiI1ZTUxNDdhMThmMGUxMzM0ODVhOTAyZDgifSwianRpIjoiNzU0MWRkMWEtN2FkYy00NjhiLWI0YjQtZTQzYjYzOTdhYzFmIiwiZnJlc2giOmZhbHNlLCJpYXQiOjE1ODQxNzAwMjgsInR5cGUiOiJhY2Nlc3MiLCJuYmYiOjE1ODQxNzAwMjgsImlkZW50aXR5IjoiNWU2NjdjMzY5ZWQ3MTg2OTViZTMwMzgxIn0.-3r9jayUDKYDjifq2WnXO1pIU02CveXV4ZECoCgG6cs"
        user = 'fran@fran.es'
        response = requests.get("http://localhost:5000/myproject/" + user, headers={'Authorization': 'Bearer ' + token})

        return response.json()

    def stract_scans(self, projects):
        scans_list = []
        for project in projects:
            scans = project['scans']
            for s in scans:
                scans_list.append(s)

        return scans_list
