from requests import Session
from Logger import logger
from time import sleep


class EroBot:
    _TELEGRAM_REQUEST_URL = 'https://api.telegram.org'
    _BOT_TOKEN = '386770232:AAEYVJB1OhHYILEzO2oUPZpASwVDxflXZLs'
    _CHAT_ID = '112106805'


    def __init__(self):
        self._session = Session()
        self.last_update_id = 384222017

    def send_test_message(self):
        url = EroBot._TELEGRAM_REQUEST_URL + '/bot' + EroBot._BOT_TOKEN + '/sendMessage'
        params = {
            'chat_id': EroBot._CHAT_ID,
            'text': 'This is the test mesage. Ignore it.'
        }
        try:
            result = self._session.get(url=url, params=params)
            logger.info(result.json())
        except Exception as e:
            logger.error(str(e))

    def send_message(self, message: str, chat_id:str=_CHAT_ID, disable_notification: bool=False):
        url = EroBot._TELEGRAM_REQUEST_URL + '/bot' + EroBot._BOT_TOKEN + '/sendMessage'
        params = {
            'chat_id': chat_id,
            'text': message,
            'disable_notification': disable_notification
        }
        try:
            result = self._session.get(url=url, params=params)
            logger.info(result.json())
        except Exception as e:
            logger.error(str(e))

    def send_file(self, path: str, disable_notification: bool=False):
        url = EroBot._TELEGRAM_REQUEST_URL + '/bot' + EroBot._BOT_TOKEN + '/sendDocument'
        with open(path, 'rb') as file:
            params = {
                'chat_id': EroBot._CHAT_ID,
                'disable_notification': disable_notification
            }
            logger.info('Sending {} to chat with id:{}'.format(path, EroBot._CHAT_ID))
            try:
                result = self._session.post(url=url, params=params, files={'document': file})
                result_json = result.json()
                if not result_json['ok']:
                    logger.warn('File uploading was unsuccessful')
                    logger.warn(result_json['description'])
            except Exception as e:
                logger.error('Error occurred during request')
                logger.error(str(e))

            sleep(2)

    def get_updates(self, offset):
        url = EroBot._TELEGRAM_REQUEST_URL + '/bot' + EroBot._BOT_TOKEN + '/getupdates'
        try:
            result = self._session.get(url=url, params={'offset': offset})
            if result.status_code == 200:
                return result.json()
        except Exception as e:
            logger.error(str(e))
            return



if __name__ == '__main__':
    pass


