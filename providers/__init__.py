"""providers """
import abc
import datetime
import random
import string
import time

import bs4
import requests

# period for checking new content on websites
CHECKING_PERIOD = datetime.timedelta(days=7)
LETTERS = [letter for letter in string.ascii_lowercase if letter != 'q']


def get_random_page_numbers(amount: int, pages_amount: int):
    """
    Get random pages
    :param int amount: amount of pages, that need to be chosen.
    :param int pages_amount: amount of available pages.
    :return list: list of randomly chosen pages.
    """
    random_pages = [random.randint(1, pages_amount) for _ in range(amount)]
    print('Random pages: ' + str(random_pages))
    return random_pages


class EroBaseProvider(abc.ABC):
    """Base class for all providers."""

    def __init__(self):
        self._request_url: str = None
        self._session: requests.Session = requests.Session()

    @property
    def request_url(self):
        """Get request url."""
        return self._request_url

    @request_url.setter
    def request_url(self, value: str):
        """Set request url."""
        self._request_url = value

    @abc.abstractmethod
    def get_random_images(self, amount):
        """
        Get random images from web site.
        :param int amount: amount of random images.
        :return list: list with urls of random images.
        """


class ErolubProvider(EroBaseProvider):
    """Provider for http://erolub.com website."""

    def __init__(self):
        super().__init__()
        self._session = requests.Session()
        self.request_url = 'http://erolub.com/photo/'
        self._page_url_template = 'page/{}/'

        self._pages_amount = 10
        self._last_time_checked = datetime.datetime.fromtimestamp(1272032894)

    def _get_pages_amount(self):
        """Get amount of pages available on website."""
        return 36

        if datetime.now() - self._last_time_checked < CHECKING_PERIOD:
            return self._pages_amount

        pages_amount = 0
        number = 0
        print('Getting pages amount...')
        response = self._session.get(url=self.request_url)
        bs = bs4.BeautifulSoup(response.text)
        pagination_element = bs.find('span', class_='navigation')
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

    def _get_posts_on_page(self, page_number):
        """
        Get all posts on given page identified by number.
        :param int page_number: number of page.
        :return list: list of posts available on given page.
        """
        page = self._page_url_template.format(page_number)
        request_url = self.request_url + page
        print('Getting post on: ' + request_url)
        response = self._session.get(url=request_url)
        bs = bs4.BeautifulSoup(response.text)
        content = bs.find('div', {'id': 'dle-content'})
        posts = content.find_all('div', class_='item-box')
        del response
        del bs
        del content
        return posts

    def get_random_images(self, amount):
        """
        Get random images from web site.
        :param int amount: amount of random images.
        :return list: list with urls of random images.
        """
        result_images_urls = []
        pages_amount = self._get_pages_amount()
        random_page_numbers = get_random_page_numbers(amount, pages_amount)

        for number in random_page_numbers:
            time.sleep(1)
            try:
                posts = self._get_posts_on_page(number)
                random_post = random.choice(posts)
                post_url = random_post.find('a', recursive=True)['href']
                print('Getting post content from: ' + post_url)
                response = self._session.get(url=post_url)
                bs = bs4.BeautifulSoup(response.text)
            except:
                continue

            gallery = bs.find('div', class_='pw-description clearfix')
            if gallery is not None:
                random_image = random.choice(gallery.find_all('img'))
                url = random_image['src']
                print('Image url: ' + url)
                result_images_urls.append('http://erolub.com/' + url)

        return result_images_urls


class EroticBeautiesProvider(EroBaseProvider):
    """Provider for http://www.eroticbeauties.net website."""

    def __init__(self):
        super().__init__()
        self._session = requests.Session()
        self.request_url = 'http://www.eroticbeauties.net/'
        self._page_url_template = 'page-{}.html'

        self._pages_amount = 10
        self._last_time_checked = datetime.datetime.fromtimestamp(1272032894)

    def _get_pages_amount(self):
        """Get amount of pages available on website."""
        if datetime.datetime.now() - self._last_time_checked < CHECKING_PERIOD:
            return self._pages_amount

        pages_amount = 0
        print('Getting pages amount...')
        response = self._session.get(url=self.request_url)
        bs = bs4.BeautifulSoup(response.text)
        paginations = bs.find_all(class_='pagination')
        pagination_element = next((pagination for pagination in paginations if len(pagination.attrs['class']) == 1))
        for element in pagination_element:
            if isinstance(element, bs4.Tag):
                try:
                    number = int(element.find('a').text)
                except:
                    pass
                if number > pages_amount:
                    pages_amount = number
        del bs
        del response
        del paginations
        print('Pages amount: ' + str(pages_amount))
        self._pages_amount = pages_amount
        return pages_amount

    def _get_posts_on_page(self, page_number):
        """
        Get all posts on given page identified by number.
        :param int page_number: number of page.
        :return list: list of posts available on given page.
        """
        page = self._page_url_template.format(page_number)
        request_url = self.request_url + page
        print('Getting post on: ' + request_url)
        response = self._session.get(url=request_url)
        bs = bs4.BeautifulSoup(response.text)
        content = bs.find('div',
                          class_='col-xs-12 col-sm-8 col-md-5 col-lg-6 pull-left text-center center-block index-content')
        posts = content.find_all('div', class_='gallery-container-V')
        del response
        del bs
        del content
        return posts

    def get_random_images(self, amount):
        """
        Get random images from web site.
        :param int amount: amount of random images.
        :return list: list with urls of random images.
        """
        result_images_urls = []
        pages_amount = self._get_pages_amount()
        random_page_numbers = get_random_page_numbers(amount, pages_amount)

        for number in random_page_numbers:
            time.sleep(2)
            try:
                posts = self._get_posts_on_page(number)
                random_post = random.choice(posts)
                post_url = random_post.find('a', recursive=True)['href']
                print('Getting post content from: ' + post_url)
                response = self._session.get(url=post_url)
                bs = bs4.BeautifulSoup(response.text)
            except:
                continue

            gallery = bs.find('div', class_='my-gallery')
            if gallery is not None:
                random_image = random.choice(gallery.find_all('figure'))
                url = random_image.find('a', recursive=True)['href']
                print('Image url: ' + url)
                result_images_urls.append(url)

        return result_images_urls


class KindGirlsProvider(EroBaseProvider):
    """Provider for http://www.kindgirls.com website."""

    def __init__(self):
        super().__init__()
        self._session = requests.Session()
        self.request_url = 'http://www.kindgirls.com/'
        self._page_url_template = 'girls/?i={}'

    def _get_models_on_page(self, letter):
        """
        Get all models on given page identified by letter.
        :param letter: letter page to search on.
        :return list: list of available models on given page.
        """
        page = self._page_url_template.format(letter)
        request_url = self.request_url + page
        print('Getting post on: ' + request_url)
        response = self._session.get(url=request_url)
        bs = bs4.BeautifulSoup(response.text)
        models = bs.find_all('div', class_='model_list')
        del response
        del bs
        return models

    def get_random_images(self, amount):
        """
        Get random images from web site.
        :param int amount: amount of random images.
        :return list: list with urls of random images.
        """
        result_images_urls = []
        random_letters = [random.choice(LETTERS) for _ in range(amount)]

        for letter in random_letters:
            time.sleep(1)
            models = self._get_models_on_page(letter)
            random_model = random.choice(models)
            model_url = self.request_url + random_model.find('a', recursive=True)['href']
            print('Getting post content from: ' + model_url)
            response = self._session.get(url=model_url)
            bs = bs4.BeautifulSoup(response.text,)
            random_model_post_url = self._request_url + random.choice(bs.find_all('div', class_='gal_list')).find('a')['href']
            response = self._session.get(url=random_model_post_url)
            bs = bs4.BeautifulSoup(response.text,)

            random_image = random.choice(bs.find_all('div', class_='gal_list'))
            random_image: str = random_image.find('img')['src'].replace('/m6', '')
            result_images_urls.append(random_image)

        return result_images_urls


class RussiaSexyGirlsProvider(EroBaseProvider):
    """Provider for https://russiasexygirls.com website."""

    def __init__(self):
        super().__init__()
        self._session = requests.Session()
        self.request_url = 'https://russiasexygirls.com'
        self._page_url_template = '/models/{}/'

    def _get_models_on_page(self, letter):
        """
        Get all models on given page identified by letter.
        :param str letter: letter page to search on.
        :return list: list of available models on given page.
        """
        page = self._page_url_template.format(letter)
        request_url = self.request_url + page
        print('Getting post on: ' + request_url)
        response = self._session.get(url=request_url)
        bs = bs4.BeautifulSoup(response.text)
        models = bs.find('ul', class_='models-list').find_all('li')
        del response
        del bs
        return models

    def get_random_images(self, amount):
        """
        Get random images from web site.
        :param int amount: amount of random images.
        :return list: list with urls of random images.
        """
        result_images_urls = []
        random_letters = [random.choice(LETTERS) for _ in range(amount)]

        for letter in random_letters:
            time.sleep(1)
            models = self._get_models_on_page(letter)
            random_model = random.choice(models)
            model_url = random_model.find('a', recursive=True)['href']
            print('Getting post content from: ' + model_url)
            response = self._session.get(url=model_url)
            bs = bs4.BeautifulSoup(response.text)
            random_model_post_url = random.choice(bs.find('div', id='main').find_all('div', class_='entry-summary')).find('a', class_='read-more-link')['href']
            response = self._session.get(url=random_model_post_url)
            bs = bs4.BeautifulSoup(response.text)

            random_image = random.choice(bs.find('div', class_='entry-summary').find_all('img'))['src']
            result_images_urls.append(random_image)

        return result_images_urls
