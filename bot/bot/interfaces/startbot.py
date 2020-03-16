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
        return self.stract_scans(projects)

    def get_projects(self):
        token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2NsYWltcyI6ImZyYW5AZnJhbi5lcyIsImp0aSI6Ijg2YjdiYjNlLWQxZmUtNDViNy1iYmRjLTJlM2FhNDEzNjhmMyIsImZyZXNoIjpmYWxzZSwiaWF0IjoxNTg0MzU3MDYwLCJ0eXBlIjoiYWNjZXNzIiwibmJmIjoxNTg0MzU3MDYwLCJpZGVudGl0eSI6IjVlNmU1ZGY1OGM4Yjg0NDVjMzFkMWUxMSJ9.MglR3AAMT9sII34iMZkvCXuv8PDODm2ojZ0uEaSUtq0"
        # Get the user
        token_decode = jwt.decode(token, verify=False)
        user = token_decode['user_claims']
        response = requests.get("http://localhost:5000/myproject/" + user, headers={'Authorization': 'Bearer ' + token})

        return response.json()

    def stract_scans(self, projects):
        scans_list = []
        for project in projects:
            scans = project['scans']
            for s in scans:
                scans_list.append(s)

        return scans_list
