"""providers for http://oboobs.ru and http://obutts.ru"""
import providers


class OBaseProvider(providers.EroBaseProvider):
    """Base provider for oboobs and obutts websites."""

    def __init__(self, request_url: str, base_url: str):
        super().__init__(request_url)
        self._base_url: str = base_url

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


class OBoobsProvider(OBaseProvider):
    """Provider for http://oboobs.ru website."""

    def __init__(self):
        super().__init__('http://api.oboobs.ru', 'http://media.oboobs.ru')


class OButtsProvider(OBaseProvider):
    """Provider for http://obutts.ru website."""

    def __init__(self):
        super().__init__('http://api.obutts.ru', 'http://media.obutts.ru')
