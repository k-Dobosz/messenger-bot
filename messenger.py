#!/usr/bin/env python
from bot import *
from python_json_config import ConfigBuilder
from selenium.webdriver.common.keys import Keys
import getopt
import logging
import sys


builder = ConfigBuilder()
config = builder.parse_config('config.json')

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)
logs = logging.FileHandler('logs.log')
logs.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logs.setFormatter(formatter)
logger.addHandler(logs)


def main():
    show_browser = False

    try:
        opts, args = getopt.getopt(sys.argv[1:], "hvs", ["help", "showbrowser"])
    except getopt.GetoptError as err:
        print(err)
    for o,a in opts:
        if o == '-v':
            logging.getLogger(__name__).setLevel(logging.DEBUG)
        elif o in ('-h', '--help'):
            sys.exit()
        elif o in ('-s', '--showbrowser'):
            show_browser = True
        else:
            assert False, 'Unhandled option'

    bot = MessengerBot(
        show_browser=show_browser,
        url=config.url,
        email=config.account.email,
        password=config.account.password
    )

    @bot.command()
    def command_all():
        m = Message(bot)
        for person in config.lists.all:
            m.mention(person)
        m.send()

    @bot.command()
    def command_girls():
        m = Message(bot)
        for person in config.lists.girls:
            m.mention(person)
        m.send()

    @bot.command()
    def command_boys():
        m = Message(bot)
        for person in config.lists.boys:
            m.mention(person)
        m.send()

    @bot.command()
    def command_help():
        m = Message(bot)
        m.add('Available commands:')
        for command in config.commands:
            m.add(Keys.ALT + Keys.ENTER)
            m.add(command)
        m.send()

    bot.run()

if __name__ == '__main__':
    main()