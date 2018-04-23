from .EroBaseProvider import EroBaseProvider

from random import randint, choice
from requests import Session
from bs4 import BeautifulSoup, Tag
from time import sleep
from datetime import datetime, timedelta

CHECKING_PERIOD = timedelta(days=7)


class EroticBeautiesProvider(EroBaseProvider):
    def __init__(self):
        super().__init__()
        self._session = Session()
        self.request_url = 'http://www.eroticbeauties.net/'
        self._page_url_template = 'page-{}.html'

        self._pages_amount = 10
        self._last_time_checked = datetime.fromtimestamp(1272032894)

    def _get_pages_amount(self):
        if datetime.now() - self._last_time_checked < CHECKING_PERIOD:
            return self._pages_amount

        pages_amount = 0
        response = self._session.get(url=self.request_url)
        bs = BeautifulSoup(response.text, 'lxml')
        paginations = bs.find_all(class_='pagination')
        pagination_element = next((pagination for pagination in paginations if len(pagination.attrs['class']) == 1))
        for element in pagination_element:
            if isinstance(element, Tag):
                try:
                    number = int(element.find('a').text)
                except:
                    pass
                if number > pages_amount:
                    pages_amount = number
        del bs
        del response
        del paginations
        self._pages_amount = pages_amount
        return pages_amount

    def _get_random_page_numbers(self, amount, pages_amount):
        random_pages = []
        for i in range(amount):
            random_page_number = randint(1, pages_amount)
            if random_page_number not in random_pages:
                random_pages.append(random_page_number)
        return random_pages

    def _get_posts_on_page(self, page_number):
        page = self._page_url_template.format(page_number)
        request_url = self.request_url + page
        response = self._session.get(url=request_url)
        bs = BeautifulSoup(response.text, 'lxml')
        content = bs.find('div',
                          class_='col-xs-12 col-sm-8 col-md-5 col-lg-6 pull-left text-center center-block index-content')
        posts = content.find_all('div', class_='gallery-container-V')
        del response
        del bs
        del content
        return posts

    def get_random_images(self, amount):
        result_images_urls = []
        pages_amount = self._get_pages_amount()
        random_page_numbers = self._get_random_page_numbers(amount, pages_amount)

        for number in random_page_numbers:
            sleep(1)
            try:
                posts = self._get_posts_on_page(number)
                random_post = choice(posts)
                response = self._session.get(url=random_post.find('a', recursive=True)['href'])
                bs = BeautifulSoup(response.text, 'lxml')
            except:
                continue

            gallery = bs.find('div', class_='my-gallery')
            random_image = choice(gallery.find_all('figure'))
            url = random_image.find('a', recursive=True)['href']
            result_images_urls.append(url)

        return result_images_urls
