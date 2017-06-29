from requests import Session

class ObuttsCrawler:
    _BASE_URL = 'http://media.obutts.ru'
    _REQUEST_URL = 'http://api.obutts.ru'


    def __init__(self):
        self._session = Session()

    def crawl_noise(self, count:int=5):
        url = ObuttsCrawler._REQUEST_URL + '/noise' + '/{count}'.format(count=count)
        response = self._session.get(url=url)
        if response.status_code == 200:
            result = response.json()

        urls = ['noise/' + element['preview'].split('/')[1] for element in result]
        return urls

