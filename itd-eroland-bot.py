from pydoc import cram
from sys import argv
from sys import exit
from os import makedirs
from os.path import dirname
from os.path import basename
from os.path import abspath
from os.path import isfile
from os.path import isdir
from os.path import exists
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


CHUNK_SIZE = 1024 * 48500
CONTENT_DIR = dirname(abspath(__file__)) + '/content'

bot = EroBot()
boobs_crawler = OboobsCrawler()
butts_crawler = ObuttsCrawler()
session = Session()

def _get_extension(content_type: str):
    extension = re.split('[/ ;]', content_type)[1]
    return '.' + extension


def save_image(url:str, path:str):
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
    if 'ok' in updates_result and updates_result['ok'] == True:
        updates = updates_result['result']
        results = []
        for update in updates:
            result = {
                'chat_id': update['message']['chat']['id'],
                'text': update['message'].get('text', ''),
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
    # # If previously removing was unsuccessful
    # clear_directory(CONTENT_DIR)
    #
    #
    # # Remove all files
    # clear_directory(CONTENT_DIR)

    while True:
        updates_result = bot.get_updates(bot.last_update_id + 1)
        if updates_result:
            for update in parse_updates(updates_result):
                bot.last_update_id = update['update_id'] if update['update_id'] > bot.last_update_id else bot.last_update_id
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


# {"ok":true,"result":[
#     {
#         "update_id":384222016,
#         "message":
#             {
#                 "message_id":12,
#                 "from":{"id":112106805,"first_name":"\u042f\u0440\u0438\u043a","last_name":"\u0420\u0435\u0448\u0435\u0442\u043d\u0438\u043a","username":"yar_resh","language_code":"en"},
#                 "chat":{"id":112106805,"first_name":"\u042f\u0440\u0438\u043a","last_name":"\u0420\u0435\u0448\u0435\u0442\u043d\u0438\u043a","username":"yar_resh","type":"private"},
#                 "date":1498651525,
#                 "text":"/help",
#                 "entities":[{"type":"bot_command","offset":0,"length":5}]}},
#     {
#         "update_id":384222017,
# "message":{"message_id":13,"from":{"id":112106805,"first_name":"\u042f\u0440\u0438\u043a","last_name":"\u0420\u0435\u0448\u0435\u0442\u043d\u0438\u043a","username":"yar_resh","language_code":"en"},"chat":{"id":112106805,"first_name":"\u042f\u0440\u0438\u043a","last_name":"\u0420\u0435\u0448\u0435\u0442\u043d\u0438\u043a","username":"yar_resh","type":"private"},"date":1498654449,"text":"/noise","entities":[{"type":"bot_command","offset":0,"length":6}]}}]}
