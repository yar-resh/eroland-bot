from scrappers.EroScrapper import EroScrapper


class ObuttsScrapper(EroScrapper):
    _BASE_URL = 'http://media.obutts.ru'
    _REQUEST_URL = 'http://api.obutts.ru'
    _COMMANDS = {
        'noise': 'Example: "noise 50" - get 50 random noise elements'
    }
    _IDENTIFIER = 'obutts'

    def get_images(self, *args):
        super().get_images(*args)

    @property
    def commands(self):
        return self._COMMANDS

    @property
    def scrapper_name(self):
        return 'Obutts (http://obutts.ru)'

    @property
    def identifier(self):
        return self._IDENTIFIER

    def get_instruction(self):
        super().get_instruction()



