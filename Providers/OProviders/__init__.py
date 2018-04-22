from .OBaseProvider import OBaseProvider


# from .OBoobsProvider import OBoobsProvider
# from .OButtsProvider import OButtsProvider


def _init_factory(request_url: str, base_url: str, base_class):
    def __init__(self):
        super(base_class, self).__init__()
        self.request_url = request_url
        self.base_url = base_url

    return __init__


OBoobsProvider = type('OBoobsProvider', (OBaseProvider,),
                      {'__init__': _init_factory('http://api.oboobs.ru', 'http://media.oboobs.ru', OBaseProvider)})
OButtsProvider = type('OButtsProvider', (OBaseProvider,),
                      {'__init__': _init_factory('http://api.obutts.ru', 'http://media.obutts.ru', OBaseProvider)})

__all__ = ['OBaseProvider', 'OBoobsProvider', 'OButtsProvider']
