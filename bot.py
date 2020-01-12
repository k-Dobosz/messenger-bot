#!/usr/bin/env python
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import chromedriver_binary
import time


class MessengerBot(object):
    def __init__(self, show_browser=False, url='', email='', password=''):
        self.available_commands = {}

        try:
            chrome_options = Options()
            if not show_browser:
                chrome_options.add_argument('--headless')
                chrome_options.add_argument('--window-size=1920x1080')
            self.driver = webdriver.Chrome(options=chrome_options)
            self.driver.get('https://www.messenger.com/t/' + url)
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="email"]')))
            self.driver.find_element_by_xpath('//*[@id="email"]')\
                .send_keys(email)
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="pass"]')))
            self.driver.find_element_by_xpath('//*[@id="pass"]')\
                .send_keys(password)
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="loginbutton"]')))
            self.driver.find_element_by_xpath('//*[@id="loginbutton"]')\
                .click()
        except NoSuchElementException:
            print('Element not found')

    def run(self):
        while True:
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//div[@class="_aok _7i2m"]')))
            message = self.driver.find_elements_by_xpath("//div[@class='_aok _7i2m']")[-1].text.lower()

            if message[0] == '!':
                message = message[1:]
                if message in self.available_commands:
                    self.available_commands[message].callback()

            time.sleep(1)

    def get_driver(self):
        return self.driver

    def send_message(self, message):
        message_box = self.driver.switch_to.active_element
        message_box.send_keys(message)
        message_box.send_keys(Keys.ENTER)

    def add_command(self, command):
        if not isinstance(command, Command):
            raise Exception('This is not a command')
        self.available_commands[command.name] = command

    def command(self, *args, **kwargs):
        def wrapper(function):
            command = Command.to_command(*args, **kwargs)(function)
            self.add_command(command)
            return command
        return wrapper


class Command(object):
    def __init__(self, function, **kwargs):
        self.name = kwargs.get('name') or function.__name__[8:]
        self.callback = function

    def callback(self):
        callback = self.callback()
        callback()

    @staticmethod
    def to_command(name=None, **kwargs):
        def wrapper(function):
            if isinstance(function, Command):
                raise Exception('This function is already a command')
            return Command(function, name=name, **kwargs)
        return wrapper


class Message(object):
    def __init__(self, bot):
        self.content = ''
        self.driver = bot.get_driver()

    def add(self, content):
        message_box = self.driver.switch_to.active_element
        message_box.send_keys(content)

    def mention(self, content):
        message_box = self.driver.switch_to.active_element
        message_box.send_keys('@' + content)
        time.sleep(0.035)
        message_box.send_keys(Keys.TAB)
        message_box.send_keys(Keys.SPACE)

    def send(self):
        message_box = self.driver.switch_to.active_element
        message_box.send_keys(Keys.ENTER)
