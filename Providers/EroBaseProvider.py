from abc import ABC, abstractmethod
from requests import Session


class EroBaseProvider(ABC):

    def __init__(self):
        self._request_url: str = None
        self._session: Session = Session()

    @property
    def request_url(self):
        return self._request_url

    @request_url.setter
    def request_url(self, value):
        self._request_url = value

    @abstractmethod
    def get_random_images(self, amount):
        ...
