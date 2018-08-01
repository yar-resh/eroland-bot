import telegram
import telegram.ext

import logger
import providers
import providers.oproviders

LOGGER = logger.logger
LOADING_URL = 'http://siski.pro/rnd/animated/125.gif'
WAIT_TEXT = 'It will take some time. So, wait patiently :)'
HELP_MESSAGE = """Welcome to <b>ITD-Eroland bot!</b>
List of commands:
<i>/boobs</i> - returns set of 5 images with boobs
<i>/butts</i> - returns 5 images with boobs (at this moment all images sends separately)
<i>/beauty</i> - returns set of 5 images from www.eroticbeauties.net
<i>/erolub</i> - returns set of 5 images from www.erolub.com/photo/
<i>/help</i> - prints help message"""


def error_handler(bot, update: telegram.Update, error):
    """Log Errors caused by Updates."""
    LOGGER.error('Update "%s" caused error "%s"', update, error)


def loading(func):
    def wrapper(self, bot: telegram.Bot, update: telegram.Update, *args, **kwargs):
        text = '{}\n\n{}'.format(WAIT_TEXT, LOADING_URL)
        try:
            message = update.message.reply_text(text, quote=False)
            func(self, bot, update)
            message.delete()
        except Exception as exc:
            print(exc)
    return wrapper


class EroBot:
    def __init__(self, access_token: str):
        self.updater = telegram.ext.Updater(access_token)
        self.boobs_provider = providers.oproviders.OBoobsProvider()
        self.butts_provider = providers.oproviders.OButtsProvider()
        self.beauty_provider = providers.EroticBeautiesProvider()
        self.erolub_provider = providers.ErolubProvider()
        self.kind_provider = providers.KindGirlsProvider()
        self.sexy_provider = providers.RussiaSexyGirlsProvider()
        self.providers = [self.boobs_provider, self.butts_provider, self.beauty_provider, self.erolub_provider, self.kind_provider]
        self._init()

    def _init(self):
        handlers = (
            telegram.ext.CommandHandler('start', self._start),
            telegram.ext.CommandHandler('help', self._help),
            telegram.ext.CommandHandler('boobs', self._boobs),
            telegram.ext.CommandHandler('butts', self._butts),
            telegram.ext.CommandHandler('beauty', self._beauty),
            telegram.ext.CommandHandler('erolub', self._erolub),
            telegram.ext.CommandHandler('kind', self._kind),
            telegram.ext.CommandHandler('sexy', self._sexy)
        )
        for handler in handlers:
            self.updater.dispatcher.add_handler(handler)
        self.updater.dispatcher.add_error_handler(error_handler)

    def _start(self, bot: telegram.Bot, update: telegram.Update):
        self._help(bot, update)

    def _help(self, bot: telegram.Bot, update: telegram.Update):
        update.message.reply_text(HELP_MESSAGE, quote=False, parse_mode='HTML', disable_web_page_preview=True)

    @loading
    def _boobs(self, bot: telegram.Bot, update: telegram.Update):
        media = [telegram.InputMediaPhoto(url) for url in self.boobs_provider.get_random_images(5)]
        bot.send_media_group(update.message.chat.id, media, disable_notification=True)

    @loading
    def _butts(self, bot: telegram.Bot, update: telegram.Update):
        media = self.butts_provider.get_random_images(5)
        for image in media:
            try:
                bot.send_photo(update.message.chat.id, image, disable_notification=True)
            except Exception as e:
                print(str(e))

        # bot.send_media_group(update.message.chat.id, media, disable_notification=True)

    @loading
    def _beauty(self, bot: telegram.Bot, update: telegram.Update):
        try:
            media = [telegram.InputMediaPhoto(url) for url in self.beauty_provider.get_random_images(5)]
            bot.send_media_group(update.message.chat.id, media, disable_notification=True)
        except Exception as e:
            print(str(e))

    @loading
    def _erolub(self, bot: telegram.Bot, update: telegram.Update):
        try:
            media = [telegram.InputMediaPhoto(url) for url in self.erolub_provider.get_random_images(5)]
            bot.send_media_group(update.message.chat.id, media, disable_notification=True)
        except Exception as e:
            print(str(e))

    @loading
    def _kind(self, bot: telegram.Bot, update: telegram.Update):
        try:
            media = [telegram.InputMediaPhoto(url) for url in self.kind_provider.get_random_images(5)]
            bot.send_media_group(update.message.chat.id, media, disable_notification=True)
        except Exception as e:
            print(str(e))

    @loading
    def _sexy(self, bot: telegram.Bot, update: telegram.Update):
        try:
            media = [telegram.InputMediaPhoto(url) for url in self.sexy_provider.get_random_images(5)]
            bot.send_media_group(update.message.chat.id, media, disable_notification=True)
        except Exception as e:
            print(str(e))

    def start_bot(self, timeout=120, idle=False):
        self.updater.start_polling(timeout=timeout)
        if idle:
            self.updater.idle()
