"""providers for http://oboobs.ru and http://obutts.ru"""
import providers


class OBaseProvider(providers.EroBaseProvider):
    """Base provider for oboobs and obutts websites."""

    def __init__(self):
        super().__init__()
        self._base_url: str = None

    def get_random_images(self, amount):
        """
        Get random images from website.
        :param int amount: amount of random images
        :return list: list with urls of random images
        """
        url = self.request_url + '/noise' + '/{amount}'.format(amount=amount)
        response = self._session.get(url=url)
        if response.status_code != 200:
            raise RuntimeError

        result = response.json()
        urls = [f'{self.base_url}/noise/{element["preview"].split("/")[1]}' for element in result]
        return urls

    @property
    def base_url(self):
        """Base url."""
        return self._base_url

    @base_url.setter
    def base_url(self, value):
        """Set base url."""
        self._base_url = value


def _init_factory(request_url: str, base_url: str, base_class):
    """Construct __init__ methods for classes derived from OBaseProvider"""

    def __init__(self):
        super(base_class, self).__init__()
        self.request_url = request_url
        self.base_url = base_url
    return __init__


OBoobsProvider = type('OBoobsProvider', (OBaseProvider,),
                      {'__init__': _init_factory('http://api.oboobs.ru', 'http://media.oboobs.ru', OBaseProvider)})
OButtsProvider = type('OButtsProvider', (OBaseProvider,),
                      {'__init__': _init_factory('http://api.obutts.ru', 'http://media.obutts.ru', OBaseProvider)})
