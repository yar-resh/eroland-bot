from sys import argv
from sys import exit
from os.path import dirname
from os.path import abspath
from os.path import isdir
from os import listdir
from os import remove
from requests import Session, codes
from hashlib import md5
from time import sleep
import re
import shutil

from Logger import logger

from EroBot import EroBot
from OboobsCrawler import OboobsCrawler
from ObuttsCrawler import ObuttsCrawler

TIMEOUT = 120

boobs_crawler = OboobsCrawler()
butts_crawler = ObuttsCrawler()
session = Session()


def _get_extension(content_type: str):
    extension = re.split('[/ ;]', content_type)[1]
    return '.' + extension


def save_image(url: str, path: str):
    response = session.get(url, stream=True)
    if response.status_code == codes.ok and response.raw:
        name = md5(url.encode()).hexdigest()
        name += _get_extension(response.headers['Content-Type'])
        full_path = path + '/' + name
        with open(full_path, 'wb') as image_file:
            response.raw.decode_content = True
            shutil.copyfileobj(response.raw, image_file)
        return name


def clear_directory(path: str):
    if not isdir(path):
        return False
    filelist = [f for f in listdir(path)]
    for f in filelist:
        full_file_name = path + '/' + f
        logger.info('Removing {}...'.format(full_file_name))
        try:
            remove(path + '/' + f)
            logger.info('ok')
        except Exception as e:
            logger.warn('Error occurred when removing {}'.format(full_file_name))
            logger.warn(str(e))
    return True


def parse_updates(updates_result):
    if 'ok' in updates_result and updates_result['ok'] is True:
        updates = updates_result['result']
        results = []
        for update in updates:
            message = update.get('message', None)
            if not message:
                message = update.get('edited_message', None)
            if message:
                result = {
                    'chat_id': message['chat']['id'],
                    'text': message.get('text', ''),
                    'update_id': update['update_id']
                }
                results.append(result)
        return results
    return []


def get_boobs():
    preview_urls = boobs_crawler.crawl_noise()
    images_url = []
    for preview in preview_urls:
        url = 'http://media.oboobs.ru/{preview}'.format(preview=preview)
        images_url.append(url)
    return images_url


def get_butts():
    preview_urls = butts_crawler.crawl_noise()
    images_url = []
    for preview in preview_urls:
        url = 'http://media.obutts.ru/{preview}'.format(preview=preview)
        images_url.append(url)
    return images_url


def main():
    if len(argv) < 2:
        logger.warning('Usage: python3 itd-eroland-bot.py <bot_token>')
        exit()

    token = argv[1]
    bot = EroBot(token=token)

    while True:
        updates_result = bot.get_updates(bot.last_update_id + 1, timeout=TIMEOUT)
        if updates_result:
            for update in parse_updates(updates_result):
                bot.last_update_id = update['update_id'] if update[
                                                                'update_id'] > bot.last_update_id else bot.last_update_id
                if update['text'] in ['/boobs', '/noise']:
                    urls = get_boobs()
                    for url in urls:
                        bot.send_message(url, update['chat_id'], disable_notification=True)
                        sleep(1)
                elif update['text'] == '/butts':
                    urls = get_butts()
                    for url in urls:
                        bot.send_message(url, update['chat_id'], disable_notification=True)
                        sleep(1)

        sleep(2)


if __name__ == '__main__':
    main()
