from sys import stdout
from logging import getLogger, DEBUG, Formatter, StreamHandler


logger = getLogger('itd-eroland-bot')
logger.setLevel(DEBUG)
logger_format = Formatter('%(asctime)s - %(levelname)s - %(message)s')
console_handler = StreamHandler(stdout)
console_handler.setFormatter(logger_format)
logger.addHandler(console_handler)
