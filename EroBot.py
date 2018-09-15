import os

import telegram
import telegram.ext

import logger
import providers
import providers.oproviders

LOGGER = logger.logger
IMAGES_NUMBER = int(os.environ.get('EROBOT_IMAGES_NUMBER', 5))
LOADING_URL = os.environ.get('EROBOT_LOADING_URL')
WAIT_TEXT = os.environ.get('EROBOT_WAIT_TEXT')
HELP_MESSAGE = """Welcome to <b>ITD-Eroland bot!</b>
List of commands:
<i>/boobs</i> - returns set of 5 images with boobs
<i>/beauty</i> - returns set of 5 images from www.eroticbeauties.net
<i>/erolub</i> - returns set of 5 images from www.erolub.com/photo/
<i>/kind</i> - returns set of 5 images http://www.kindgirls.com
<i>/sexy</i> - returns set of 5 images https://russiasexygirls.com
<i>/help</i> - prints help message"""


def error_handler(bot, update: telegram.Update, error):
    """Log Errors caused by Updates."""
    LOGGER.error('Update "%s" caused error "%s"', update, error)


def provider_handler(provider: providers.EroBaseProvider):
    def wrapper(bot: telegram.Bot, update: telegram.Update):
        text = '{}\n\n{}'.format(WAIT_TEXT, LOADING_URL)
        try:
            message = update.message.reply_text(text, quote=False, disable_notification=True)
            media = [telegram.InputMediaPhoto(url) for url in provider.get_random_images(IMAGES_NUMBER)]
            bot.send_media_group(update.message.chat.id, media, disable_notification=True)
            message.delete()
        except Exception as exc:
            LOGGER.error('Error occurred during processing command.\n%s"', str(exc))
    return wrapper


class EroBot:
    def __init__(self, access_token: str):
        self.updater = telegram.ext.Updater(access_token)
        self.boobs_provider = providers.oproviders.OBoobsProvider()
        self.beauty_provider = providers.EroticBeautiesProvider()
        self.erolub_provider = providers.ErolubProvider()
        self.kind_provider = providers.KindGirlsProvider()
        self.sexy_provider = providers.RussiaSexyGirlsProvider()
        self.providers = [self.boobs_provider, self.beauty_provider, self.erolub_provider, self.kind_provider]
        self._init()

    def _init(self):
        handlers = (
            telegram.ext.CommandHandler('start', self._start),
            telegram.ext.CommandHandler('help', self._help),
            telegram.ext.CommandHandler('boobs', provider_handler(self.boobs_provider)),
            telegram.ext.CommandHandler('beauty', provider_handler(self.beauty_provider)),
            telegram.ext.CommandHandler('erolub', provider_handler(self.erolub_provider)),
            telegram.ext.CommandHandler('kind', provider_handler(self.kind_provider)),
            telegram.ext.CommandHandler('sexy', provider_handler(self.sexy_provider))
        )
        for handler in handlers:
            self.updater.dispatcher.add_handler(handler)
        self.updater.dispatcher.add_error_handler(error_handler)

    def _start(self, bot: telegram.Bot, update: telegram.Update):
        self._help(bot, update)

    def _help(self, bot: telegram.Bot, update: telegram.Update):
        update.message.reply_text(HELP_MESSAGE, quote=False, parse_mode='HTML', disable_web_page_preview=True)

    def start_bot(self, timeout=120, idle=False):
        self.updater.start_polling(timeout=timeout)
        if idle:
            self.updater.idle()
