from sys import argv

from EroBot import EroBot


def main():
    key = argv[1]
    bot = EroBot(key)
    bot.start_bot(idle=True)


if __name__ == '__main__':
    main()
