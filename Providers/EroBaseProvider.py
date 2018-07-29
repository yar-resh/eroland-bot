import abc

import requests


class EroBaseProvider(abc.ABC):

    def __init__(self):
        self._request_url: str = None
        self._session: requests.Session = requests.Session()

    @property
    def request_url(self):
        return self._request_url

    @request_url.setter
    def request_url(self, value):
        self._request_url = value

    @abc.abstractmethod
    def get_random_images(self, amount):
        ...
