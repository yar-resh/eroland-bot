"""Base class for all providers."""
import abc

import requests


class EroBaseProvider(abc.ABC):
    """Base class for all providers."""

    def __init__(self):
        self._request_url: str = None
        self._session: requests.Session = requests.Session()

    @property
    def request_url(self):
        """Get request url."""
        return self._request_url

    @request_url.setter
    def request_url(self, value: str):
        """Set request url."""
        self._request_url = value

    @abc.abstractmethod
    def get_random_images(self, amount):
        """
        Get random images from web site.
        :param int amount: amount of random images.
        :return list: list with urls of random images.
        """
