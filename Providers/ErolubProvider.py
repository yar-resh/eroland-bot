from .EroBaseProvider import EroBaseProvider

from random import randint, choice
from requests import Session
from bs4 import BeautifulSoup, Tag
from time import sleep
from datetime import datetime, timedelta

CHECKING_PERIOD = timedelta(days=7)


class ErolubProvider(EroBaseProvider):
    def __init__(self):
        super().__init__()
        self._session = Session()
        self.request_url = 'http://erolub.com/photo/'
        self._page_url_template = 'page/{}/'

        self._pages_amount = 10
        self._last_time_checked = datetime.fromtimestamp(1272032894)

    def _get_pages_amount(self):
        if datetime.now() - self._last_time_checked < CHECKING_PERIOD:
            return self._pages_amount

        pages_amount = 0
        number = 0
        print('Getting pages amount...')
        response = self._session.get(url=self.request_url)
        bs = BeautifulSoup(response.text, 'lxml')
        pagination_element = bs.find(class_='navigation')
        for element in pagination_element:
            if isinstance(element, Tag):
                try:
                    number = int(element.text)
                except:
                    pass
                if number > pages_amount:
                    pages_amount = number
        del bs
        del response
        del pagination_element
        print('Pages amount: ' + str(pages_amount))
        self._pages_amount = pages_amount
        return pages_amount

    def _get_random_page_numbers(self, amount, pages_amount):
        random_pages = []
        for i in range(amount):
            random_page_number = randint(1, pages_amount)
            if random_page_number not in random_pages:
                random_pages.append(random_page_number)
        print('Random pages: ' + str(random_pages))
        return random_pages

    def _get_posts_on_page(self, page_number):
        page = self._page_url_template.format(page_number)
        request_url = self.request_url + page
        print('Getting post on: ' + request_url)
        response = self._session.get(url=request_url)
        bs = BeautifulSoup(response.text, 'lxml')
        content = bs.find('div', {'id': 'dle-content'})
        posts = content.find_all('div', class_='item-box')
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
                post_url = random_post.find('a', recursive=True)['href']
                print('Getting post content from: ' + post_url)
                response = self._session.get(url=post_url)
                bs = BeautifulSoup(response.text, 'lxml')
            except:
                continue

            gallery = bs.find('div', class_='pw-description clearfix')
            if gallery is not None:
                random_image = choice(gallery.find_all('img'))
                url = random_image['src']
                print('Image url: ' + url)
                result_images_urls.append('http://erolub.com/' + url)

        return result_images_urls
