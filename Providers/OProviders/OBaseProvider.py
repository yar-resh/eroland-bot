from Providers import EroBaseProvider


class OBaseProvider(EroBaseProvider):

    def __init__(self):
        super().__init__()
        self._base_url: str = None

    def get_random_images(self, amount):
        url = self.request_url + '/noise' + '/{amount}'.format(amount=amount)
        response = self._session.get(url=url)
        if response.status_code != 200:
            raise RuntimeError

        result = response.json()
        urls = [f'{self.base_url}/noise/{element["preview"].split("/")[1]}' for element in result]
        return urls

    @property
    def base_url(self):
        return self._base_url

    @base_url.setter
    def base_url(self, value):
        self._base_url = value