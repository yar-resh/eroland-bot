from .EroBaseProvider import EroBaseProvider

from random import randint, choice
from requests import Session
from bs4 import BeautifulSoup, Tag
from time import sleep
import string

LETTERS = [letter for letter in string.ascii_lowercase if letter != 'q']


class KindGirlsProvider(EroBaseProvider):
    def __init__(self):
        super().__init__()
        self._session = Session()
        self.request_url = 'http://www.kindgirls.com/'
        self._page_url_template = 'girls/?i=m'

    def _get_models_on_page(self, letter):
        page = self._page_url_template.format(letter)
        request_url = self.request_url + page
        print('Getting post on: ' + request_url)
        response = self._session.get(url=request_url)
        bs = BeautifulSoup(response.text)
        models = bs.find_all('div', class_='model_list')
        del response
        del bs
        return models

    def get_random_images(self, amount):
        result_images_urls = []
        random_letters = [choice(LETTERS) for _ in range(amount)]

        for letter in random_letters:
            sleep(1)
            models = self._get_models_on_page(letter)
            random_model = choice(models)
            model_url = self.request_url + random_model.find('a', recursive=True)['href']
            print('Getting post content from: ' + model_url)
            response = self._session.get(url=model_url)
            bs = BeautifulSoup(response.text,)
            random_model_post_url = self._request_url + choice(bs.find_all('div', class_='gal_list')).find('a')['href']
            response = self._session.get(url=random_model_post_url)
            bs = BeautifulSoup(response.text,)

            random_image = choice(bs.find_all('div', class_='gal_list'))
            random_image: str = random_image.find('img')['src'].replace('/m6', '')
            result_images_urls.append(random_image)

        return result_images_urls
