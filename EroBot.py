from requests import Session
from Logger import logger
from time import sleep


class EroBot:
    _TELEGRAM_REQUEST_URL = 'https://api.telegram.org'

    def __init__(self, token: str):
        self._token = token
        self._session = Session()
        self.last_update_id = 0

    def _build_request_url(self, method_name: str):
        return '{base_url}/bot{token}/{method}'.format(
            base_url = EroBot._TELEGRAM_REQUEST_URL,
            token = self._token,
            method = method_name
        )

    def send_message(self, message: str, chat_id: str, disable_notification: bool=False):
        url = self._build_request_url(method_name='sendMessage')
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

    def send_file(self, path: str, chat_id: str, disable_notification: bool=False):
        url = self._build_request_url(method_name='sendDocument')
        with open(path, 'rb') as file:
            params = {
                'chat_id': chat_id,
                'disable_notification': disable_notification
            }
            logger.info('Sending {} to chat with id:{}'.format(path, chat_id))
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

    def get_updates(self, offset: int=0, timeout: int=0):
        url = self._build_request_url(method_name='getUpdates')
        try:
            result = self._session.get(url=url, params={'offset': offset, 'timeout': timeout})
            if result.status_code == 200:
                return result.json()
            else:
                logger.error(result.text)
                return None
        except Exception as e:
            logger.error(str(e))
            return None



