from sys import argv
from sys import exit
from os.path import isdir
from os import listdir
from os import remove
from requests import Session, codes
from hashlib import md5
import re
import shutil
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler, CallbackQueryHandler,
                          ConversationHandler)
from telegram import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, ParseMode

from Logger import logger

from EroBot import EroBot
from OboobsCrawler import OboobsCrawler
from ObuttsCrawler import ObuttsCrawler

TIMEOUT = 120

boobs_crawler = OboobsCrawler()
butts_crawler = ObuttsCrawler()
session = Session()


MAIN_MENU = range(1)

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


def get_boobs(count=5):
    preview_urls = boobs_crawler.crawl_noise(count)
    images_url = []
    for preview in preview_urls:
        url = 'http://media.oboobs.ru/{preview}'.format(preview=preview)
        images_url.append(url)
    return images_url


def get_butts(count=5):
    preview_urls = butts_crawler.crawl_noise(count)
    images_url = []
    for preview in preview_urls:
        url = 'http://media.obutts.ru/{preview}'.format(preview=preview)
        images_url.append(url)
    return images_url


def error(bot, update, error):
    logger.error('Update "%s" caused error "%s"' % (update, error))


def start(bot, update):
    reply_message = '''<b>Welcome to Eroland</b>\n\nThere you can find cool boobs, nice butts and other ero content.
Use the menu below to get some cool pic '''
    reply_keyboard = get_main_keyboard()
    reply_markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True, one_time_keyboard=False)
    update.message.reply_text(reply_message, reply_markup=reply_markup, parse_mode=ParseMode.HTML)
    return MAIN_MENU


def show_boobs_menu(bot, update):
    chat_id=update.message.chat_id
    text = 'How many boobs do you want?'
    reply_markup = InlineKeyboardMarkup(get_boobs_keyboard())
    bot.send_message(text=text, chat_id=chat_id, reply_markup=reply_markup)


def show_butts_menu(bot, update):
    chat_id = update.message.chat_id
    text = 'How many butts do you want?'
    reply_markup = InlineKeyboardMarkup(get_butts_keyboard())
    bot.send_message(text=text, chat_id=chat_id, reply_markup=reply_markup)


def send_content(bot, update):
    chat_id = update.callback_query.message.chat_id
    data = update.callback_query.data
    splitted_data = data.split('/')
    resource = splitted_data[0]
    amount = splitted_data[1]

    if resource == 'oboobs':
        boobs = get_boobs(int(amount))
        for content in boobs:
            bot.send_message(chat_id=chat_id, text=content)
    if resource == 'obutts':
        butts = get_butts(int(amount))
        for content in butts:
            bot.send_message(chat_id=chat_id, text=content)


def dummy(bot, update):
    chat_id = update.callback_query.message.chat_id
    text = 'o_O'
    bot.send_message(chat_id=chat_id, text=text)


def get_main_keyboard():
    # TODO: remove hardcode and add autoloading
    keyboard = [['Boobs', 'Butts']]
    return keyboard


def get_boobs_keyboard():
    keyboard = [[InlineKeyboardButton(text='5 random boobs (oboobs.ru)', callback_data='oboobs/5'),
                 InlineKeyboardButton(text='10 random boobs (oboobs.ru)', callback_data='oboobs/10'),
                 InlineKeyboardButton(text='15 random boobs (oboobs.ru)', callback_data='oboobs/15')],

                [InlineKeyboardButton(text='dummy', callback_data='dummy'),
                 InlineKeyboardButton(text='dummy', callback_data='dummy'),
                 InlineKeyboardButton(text='dummy', callback_data='dummy')]]

    return keyboard


def get_butts_keyboard():
    keyboard = [[InlineKeyboardButton(text='5 random butts (obutts.ru)', callback_data='obutts/5'),
                 InlineKeyboardButton(text='10 random butts (obutts.ru)', callback_data='obutts/10'),
                 InlineKeyboardButton(text='15 random butts (obutts.ru)', callback_data='obutts/15')],

                [InlineKeyboardButton(text='dummy', callback_data='dummy'),
                 InlineKeyboardButton(text='dummy', callback_data='dummy'),
                 InlineKeyboardButton(text='dummy', callback_data='dummy')]]

    return keyboard


def main():
    if len(argv) < 2:
        logger.warning('Usage: python3 itd-eroland-bot.py <bot_token>')
        exit()

    token = argv[1]
    # Create the Updater and pass it your bot's token.
    updater = Updater(token)

    dp = updater.dispatcher

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler('start', start)
        ],

        states={
            MAIN_MENU: [
                RegexHandler('^(Boobs)$', show_boobs_menu),
                RegexHandler('^(Butts)$', show_butts_menu),
                CallbackQueryHandler(pattern='^(dummy)$', callback=dummy),
                CallbackQueryHandler(pattern='^(oboobs/5|oboobs/10|oboobs/15)$', callback=send_content),
                CallbackQueryHandler(pattern='^(obutts/5|obutts/10|obutts/15)$', callback=send_content)
            ]
        },

        fallbacks=[]
    )

    dp.add_handler(conv_handler)

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
