from scrappers.EroScrapper import EroScrapper


class OboobsScrapper(EroScrapper):
    _BASE_URL = 'http://media.oboobs.ru'
    _REQUEST_URL = 'http://api.oboobs.ru'
    _COMMANDS = {
        'noise': 'Example: "noise 50" - get 50 random noise elements'
    }
    _IDENTIFIER = 'oboobs'

    def __init__(self): pass

    def get_images(self, *args):
        super().get_images(*args)

    @property
    def commands(self):
        return self._COMMANDS

    @property
    def scrapper_name(self):
        return 'Oboobs (http://oboobs.ru)'

    @property
    def identifier(self):
        return self._IDENTIFIER

    def get_instruction(self):
        instruction = self.scrapper_name + '\n'
        instruction += str.join("", [
            "/{identifier} {command}:\t\t{usage}\n".format(
                command=command,
                usage=usage,
                identifier=self.identifier) for command, usage in self._COMMANDS.items()
            ])
        return instruction

o = OboobsScrapper()
print(o.get_instruction())
